from flask import Flask, jsonify, render_template
import pandas as pd
import urllib.request

app = Flask(__name__)

# ✅ Google Sheet published link (CSV output)
EXCEL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPIR5j2TyzJAorJsGX9reIhOXQKrTfyDbbv2GreXPDf2nWcBCddhoedW93yEaK1S93imugCke-dRD_/pub?output=csv"

@app.route('/')
def home():
    return render_template("index.html")   # make sure your html file is named 'index.html' and placed in 'templates' folder

@app.route('/data/<month>')
def get_month_data(month):
    try:
        # ✅ Read live data from Google Sheets
        df = pd.read_csv(EXCEL_URL)

        # ✅ Clean headers and data
        df.columns = df.columns.str.strip().str.upper()
        month = month.strip().upper()

        # ✅ Find the row for that month
        month_row = df[df['MONTH'] == month]

        if month_row.empty:
            return jsonify({})

        row = month_row.iloc[0].to_dict()

        # ✅ Ensure all values are converted to strings (safe for JSON)
        data = {
            "PAID": str(row.get("PAID", "-")),
            "NO. OF DAYS IN MONTH": str(row.get("NO. OF DAYS IN MONTH", "-")),
            "NO. OF DAYS ABSENT": str(row.get("NO. OF DAYS ABSENT", "-")),
            "NO. OF DAYS COMING": str(row.get("NO. OF DAYS COMING", "-")),
            "AMOUNT": str(row.get("AMOUNT", "-")),
            "PAYMENT MODE": str(row.get("PAYMENT MODE", "-"))
        }

        return jsonify(data)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render gives PORT automatically
    app.run(host='0.0.0.0', port=port)








