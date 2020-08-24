from saleapp import app
from saleapp.models import Category, Product
from functools import wraps
import json
import os
import hashlib


def read_products(keyword=None, from_price=None, to_price=None):
    products = Product.query

    if keyword:
        products = products.filter(Product.name.contains(keyword))

    if from_price and to_price:
        products = products.filter(Product.price.__gt__(from_price), Product.price__lt__(to_price))

    return products.all()


def read_product_by_id(product_id):
    products = read_products()
    for p in products:
        if p["id"] == product_id:
            return p

    return None


def del_product(product_id):
    products = read_products()

    for idx, p in enumerate(products):
        if p["id"] == product_id:
            del products[idx]
            break

    return update_product_json(products)


def update_product(product_id, name, description, price, image, category):
    products = read_products()
    for p in products:
        if p["id"] == int(product_id):
            p["name"] = name
            p["description"] = description
            p["price"] = float(price)
            p["image"] = image
            p["category_id"] = int(category)

            break

    return update_product_json(products)


def delete_product(product_id):
    products = read_products()
    for idx, p in enumerate(products):
        if p["id"] == int(product_id):
            del products[idx]
            break

    return update_product_json(products)


def add_product(name, description, price, image, category):
    products = read_products()
    products.append({
        "id": len(products) + 1,
        "name": name,
        "description": description,
        "price": float(price),
        "image": image,
        "category_id": int(category)
    })

    return update_product_json(products)


def update_product_json(products):
    try:
        with open(os.path.join(app.root_path, "data/products.json"), "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

        return True
    except Exception as ex:
        print(ex)
        return False


def read_categories():
    return Category.query.all()


def read_products_by_cate_id(cate_id):
    return Category.query.get(cate_id).products


def load_users():
    with open(os.path.join(app.root_path, "data/users.json"), encoding="utf-8") as f:
        return json.load(f)


def add_user(name, username, password):
    users = load_users()
    user = {
        "id": len(users) + 1,
        "name": name.strip(),
        "username": username.strip(),
        "password": str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    }
    users.append(user)

    with open(os.path.join(app.root_path, "data/users.json"), "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    return user


def check_login(username, password):
    users = load_users()

    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    for u in users:
        if u["username"].strip() == username.strip() and u["password"] == password:
            return u

    return None


if __name__ == "__main__":
    print(read_products())
