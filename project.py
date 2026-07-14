import pandas as pd
import numpy as np

df = pd.read_csv("Sales.csv", encoding="latin1")

df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

print("Missing Values")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

df.drop_duplicates(inplace=True)

df.drop(columns=["Row ID"], inplace=True)

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.month_name()
df["Quarter"] = df["Order Date"].dt.quarter
df["Week"] = df["Order Date"].dt.isocalendar().week
df["Day"] = df["Order Date"].dt.day

df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

df["Profit Margin"] = (df["Profit"] / df["Sales"]) * 100

repeat_customers = (
    df.groupby("Customer ID")["Order ID"]
      .nunique()
      .reset_index(name="Total Orders")
)

repeat_customers["Repeat Customer"] = np.where(
    repeat_customers["Total Orders"] > 1,
    "Yes",
    "No"
)

df = df.merge(
    repeat_customers[["Customer ID", "Repeat Customer"]],
    on="Customer ID",
    how="left"
)

total_sales = df["Sales"].sum()
print("Total Sales =", total_sales)

total_profit = df["Profit"].sum()
print("Total Profit =", total_profit)

total_orders = df["Order ID"].nunique()
print("Total Orders =", total_orders)

total_customers = df["Customer ID"].nunique()
print("Total Customers =", total_customers)

repeat_count = (
    repeat_customers[
        repeat_customers["Repeat Customer"] == "Yes"
    ].shape[0]
)

print("Repeat Customers =", repeat_count)

aov = total_sales / total_orders
print("Average Order Value =", round(aov, 2))

ltv = (
    df.groupby("Customer ID")["Sales"]
      .sum()
      .mean()
)

print("Customer Lifetime Value =", round(ltv, 2))

top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\nTop Products")
print(top_products)

top_categories = (
    df.groupby("Category")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTop Categories")
print(top_categories)

top_subcategories = (
    df.groupby("Sub-Category")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTop Sub-Categories")
print(top_subcategories)

customer_segment = (
    df.groupby("Customer ID")
      .agg(
          Frequency=("Order ID", "nunique"),
          Monetary=("Sales", "sum")
      )
)

print("\nCustomer Segmentation")
print(customer_segment.head())

df.to_csv("Clean_Sales.csv", index=False)

print("\nClean_Sales.csv saved successfully!")