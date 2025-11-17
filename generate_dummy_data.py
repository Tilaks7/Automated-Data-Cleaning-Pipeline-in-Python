import pandas as pd
import numpy as np
import random
from faker import Faker
import os

fake = Faker()

os.makedirs("data/raw", exist_ok=True)

num_records = 1000
categories = ['Electronics', 'Clothing', 'Home', 'Sports', None]
products = ['Laptop', 'Smartphone', 'Shoes', 'Blender', 'Football', 'T-shirt']

data = []
for i in range(num_records):
    order_id = random.randint(1000, 1100)
    order_date = fake.date_between(start_date='2023-01-01', end_date='2023-12-31')
    if random.random() < 0.05:
        order_date = None
    name = fake.name()
    if random.random() < 0.1:
        name = " " + name + " "
    product = random.choice(products)
    if random.random() < 0.1:
        product = product.lower()
    if random.random() < 0.05:
        product = product + "x"
    category = random.choice(categories)
    quantity = random.choice([random.randint(1, 10), 100])
    price = random.choice([round(random.uniform(100, 5000), 2), np.nan])
    city = random.choice(["Mumbai", "Delhi", "bangalore", " pune ", "Chennai", None])
    total = None if random.random() < 0.2 else round(quantity * (price if price else 0), 2)
    data.append([order_id, order_date, name, product, category, quantity, price, total, city])

df = pd.DataFrame(data, columns=[
    "Order_ID", "Order_Date", "Customer_Name", "Product", "Category", "Quantity", "Price", "Total", "City"
])

df.to_csv("data/raw/sample_data.csv", index=False)
print("Dummy data generated: data/raw/sample_data.csv")
