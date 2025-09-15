from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Load mock fittings data from JSON file
with open('fittings_data.json') as f:
    MOCK_FITTINGS = json.load(f)

def check_fitting_status(fitting):
    alerts = []
    supply_date = datetime.strptime(fitting['supply_date'], "%Y-%m-%d")
    warranty_expiry = supply_date + timedelta(months=fitting['warranty_period_months'])

    if datetime.today() > warranty_expiry:
        alerts.append("⚠️ Warranty Expired")

    if fitting['failure_count'] > 1:
        alerts.append("⚠️ Multiple Failures – At Risk")

    return alerts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    fitting_id = data.get('fitting_id')

    fitting = MOCK_FITTINGS.get(fitting_id)

    if not fitting:
        return jsonify({'error': 'Fitting not found'}), 404

    alerts = check_fitting_status(fitting)

    response = {
        'fitting_id': fitting_id,
        'vendor': fitting['vendor'],
        'supply_date': fitting['supply_date'],
        'warranty_period_months': fitting['warranty_period_months'],
        'inspection_dates': fitting['inspection_dates'],
        'failure_count': fitting['failure_count'],
        'alerts': alerts
    }

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
