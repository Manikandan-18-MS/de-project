import json
import os
import random
from datetime import datetime

import boto3
from faker import Faker


def generate_orders(run_date: str, n: int = 500):
    """Generate fake orders for one date. Same date = same data (idempotent)."""
    seed = int(run_date.replace("-", ""))
    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)

    statuses = ["placed", "shipped", "delivered", "cancelled"]
    categories = ["electronics", "books", "fashion", "home", "toys"]

    orders = []
    for i in range(n):
        orders.append({
            "order_id": f"{run_date.replace('-', '')}-{i:05d}",
            "customer_id": random.randint(1, 200),
            "customer_name": fake.name(),
            "city": fake.city(),
            "product_category": random.choice(categories),
            "quantity": random.randint(1, 5),
            "unit_price": round(random.uniform(5, 500), 2),
            "status": random.choice(statuses),
            "order_timestamp": f"{run_date}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00",
        })
    return orders


def extract_orders(run_date: str = None):
    run_date = run_date or datetime.utcnow().strftime("%Y-%m-%d")
    bucket = os.environ["S3_BUCKET"]
    key = f"raw/orders/ingest_date={run_date}/orders.json"

    orders = generate_orders(run_date)
    body = "\n".join(json.dumps(o) for o in orders)

    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8"))
    print(f"Uploaded {len(orders)} orders to s3://{bucket}/{key}")
    return key


if __name__ == "__main__":
    extract_orders()