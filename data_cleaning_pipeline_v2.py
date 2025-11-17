import pandas as pd
import numpy as np
import os
import argparse
import logging

logging.basicConfig(filename='logs/cleaning_log.txt',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def clean_data(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded {file_path} with {df.shape[0]} rows")

        # 1. Remove duplicates
        df.drop_duplicates(inplace=True)

        # 2. Handle missing values for numeric columns later after conversions
        # Standardize text
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip().str.lower()

        # Convert date columns
        for col in df.columns:
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Convert numeric columns
        for col in ['Quantity', 'Price', 'Total']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Handle missing numeric values: median imputation
        for col in df.select_dtypes(include=['float64','int64']).columns:
            df[col].fillna(df[col].median(), inplace=True)

        # Validate numeric ranges
        if 'Quantity' in df.columns:
            df['Quantity'] = df['Quantity'].apply(lambda x: np.nan if x <= 0 or x > 50 else x)
            df['Quantity'].fillna(df['Quantity'].median(), inplace=True)
        if 'Price' in df.columns:
            df['Price'] = df['Price'].apply(lambda x: np.nan if x <= 0 else x)
            df['Price'].fillna(df['Price'].median(), inplace=True)

        # Recalculate Total
        if all(col in df.columns for col in ['Quantity','Price']):
            df['Total'] = (df['Quantity'] * df['Price']).round(2)

        # Remove outliers using IQR for numeric columns
        numeric_cols = df.select_dtypes(include=['float64','int64']).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            if IQR > 0:
                df = df[(df[col] >= Q1 - 1.5*IQR) & (df[col] <= Q3 + 1.5*IQR)]

        # Derived columns
        if 'Order_Date' in df.columns:
            df['Order_Month'] = df['Order_Date'].dt.to_period('M').astype(str)
        if 'Total' in df.columns:
            df['Revenue_Category'] = pd.cut(
                df['Total'],
                bins=[-1, 1000, 5000, df['Total'].max()],
                labels=['Low', 'Medium', 'High']
            )

        logging.info("Data cleaned and enriched successfully.")
        return df

    except Exception as e:
        logging.error(f"Error cleaning data: {e}")
        raise

def generate_summary(df, output_folder, filename):
    try:
        os.makedirs(output_folder, exist_ok=True)
        summary = df.groupby(['Category', 'City'], dropna=False)['Total'].agg(['count', 'sum', 'mean']).reset_index()
        summary.rename(columns={'count': 'Num_Orders', 'sum': 'Total_Revenue', 'mean': 'Avg_Order_Value'}, inplace=True)
        summary.to_csv(os.path.join(output_folder, f"summary_{filename}"), index=False)
        logging.info(f"Generated summary file: summary_{filename}")
    except Exception as e:
        logging.error(f"Error creating summary: {e}")

def main(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        if file.endswith('.csv'):
            cleaned_df = clean_data(os.path.join(input_folder, file))
            cleaned_file = f"cleaned_{file}"
            cleaned_df.to_csv(os.path.join(output_folder, cleaned_file), index=False)
            generate_summary(cleaned_df, output_folder, cleaned_file)
            logging.info(f"Saved cleaned and summarized file for {file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Data Cleaning & Summarization Pipeline")
    parser.add_argument("--input", default="data/raw", help="Path to raw data folder")
    parser.add_argument("--output", default="data/cleaned", help="Path to cleaned data folder")
    args = parser.parse_args()
    main(args.input, args.output)
