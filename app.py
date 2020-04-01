from flask import Flask, jsonify
import json

app = Flask(__name__)


def open_file_level(filename):
    with open(filename) as input:
        data = json.load(input)
    return data


def discount_apply(article, discounts):
    """Some products are discounted because of a deal we made with the supplier.
    There are two kinds of discounts: - a direct cut to the article's price, e.g. get 50€
    off your 300€ caviar tin and only pay 250€ - a percentage discount, e.g. get 20% off your
    5€ creme fraiche and only pay 4€
    """

    discount_applied = article['price']
    for discount in discounts:
        if article["id"] == discount["article_id"]:
            if discount["type"] == "amount":
                discount_applied = article['price'] - discount["value"]
            else:
                discount_applied = int(article['price'] * (1 - (discount["value"] / 100)))

    return discount_applied


def calc_delivery_fee(total, delivery_fees):
    """Cost of delivery depends on how much we charged the custormer for their cart’s contents
    The more the customer spends, the less they are charged for shipping.
    """

    for delivery_fee in delivery_fees:
        min_price = delivery_fee['eligible_transaction_volume']["min_price"]

        max_price = delivery_fee['eligible_transaction_volume']["max_price"] \
            if delivery_fee['eligible_transaction_volume']["max_price"] is not None else 0

        price = int(delivery_fee['price'])

        if int(min_price) < total < int(max_price):
            total = total + price
            return total

    return total


def total_amount(cart, articles, delivery_fees=None, discounts=None):
    """We are building an e-commerce website. Our customers can: - add articles to a virtual cart -
    checkout the cart contents - get it delivered the next day
    The customer is charged the sum of the prices of each article in their cart.
    Prices are expressed in cents.
    """

    total = 0
    for items in cart["items"]:
        discount_applied = 0
        for article in articles:
            if article["id"] == items["article_id"]:
                if discounts:
                    discount_applied += discount_apply(article, discounts)
                else:
                    discount_applied = article["price"]
                total += discount_applied * items["quantity"]
    if delivery_fees:
        total = calc_delivery_fee(total, delivery_fees)

    return total


@app.route('/<level>', methods=['GET'])
def home(level):
    filename = f"{level}/data.json"
    data = open_file_level(filename)
    articles = data.get("articles")
    carts = data.get("carts")
    delivery_fees = data.get("delivery_fees", None)
    discounts = data.get("discounts", None)
    cart_sum = []
    output = {"carts": []}

    for cart in carts:
        cart_sum.append(
            {
                'id': cart['id'],
                'total': total_amount(cart, articles, delivery_fees, discounts)
            })
    output["carts"] = cart_sum

    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
