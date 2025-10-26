from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPIR5j2TyzJAorJsGX9reIhOXQKrTfyDbbv2GreXPDf2nWcBCddhoedW93yEaK1S93imugCke-dRD_/pub?output=csv"

def get_month_data(month_name):
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        df.columns = df.columns.str.strip().str.upper()
        month_name = month_name.strip().upper()

        if 'MONTH' not in df.columns:
            print("⚠️ Error: 'MONTH' column not found in sheet.")
            return None

        month_row = df[df['MONTH'].str.strip().str.upper() == month_name]
        if month_row.empty:
            print(f"No data found for month: {month_name}")
            return None

        return month_row.iloc[0].to_dict()
    except Exception as e:
        print("Error fetching sheet:", e)
        return None


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/month/<month_name>')
def month_data(month_name):
    data = get_month_data(month_name)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": f"No data found for {month_name}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

