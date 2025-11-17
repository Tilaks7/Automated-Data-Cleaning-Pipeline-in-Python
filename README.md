# 🧹 Automated Data Cleaning Pipeline in Python

This project automates the entire data cleaning and preprocessing workflow using Python. It takes raw CSV files (like e-commerce or sales data), cleans and enriches them, and generates a Power BI–ready summary output automatically.

---

## 🚀 Features
- Handles missing values and duplicates  
- Standardizes text and date formats  
- Detects and removes outliers using IQR  
- Validates numeric ranges (Quantity, Price)  
- Recalculates totals correctly  
- Creates derived columns: `Order_Month`, `Revenue_Category`  
- Generates summarized report by Category & City  
- Fully logged process for transparency

---

## 📂 Project Structure
automated-data-cleaning-pipeline/
├── data/
│ ├── raw/ # Input CSV files
│ └── cleaned/ # Cleaned outputs
├── logs/ # Log files
├── scripts/
│ ├── generate_dummy_data.py
│ └── data_cleaning_pipeline_v2.py
├── requirements.txt
└── README.md

## ⚙️ Quickstart
1. Clone the repo
2. (Optional) Create a virtual environment and activate it
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Generate dummy data (optional, a sample CSV is already included):
```
python scripts/generate_dummy_data.py
```
5. Run the cleaning pipeline:
```
python scripts/data_cleaning_pipeline_v2.py --input data/raw --output data/cleaned
```


📬 **Looking for IT Support/Technical support roles with automation skills?**  
This project shows my ability to build scalable data preprocessing systems using Python and Pandas.  
Contact: [LinkedIn](https://www.linkedin.com/71l4k) • [TNBShare.com](https://TNBShare.com)

