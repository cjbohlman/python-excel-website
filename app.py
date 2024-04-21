from flask import Flask, request, abort, render_template
import xlwings as xw
import os

def validate_inputs(weight, gender, height, cadence, pace_min, pace_sec, slope, strike, headwind, surface):
    # Validate weight
    if weight < 25 or weight > 100:
        return "Weight must be between 25 and 100 kg."

    # Validate gender
    if not gender:
        return "Please select a gender."

    # Validate height
    if height < 0 or height > 3:
        return "Height must be between 0 and 3 meters."

    # Validate cadence
    if cadence <= 0:
        return "Cadence must be a positive number."

    # Validate pace
    if pace_min < 0 or pace_sec < 0 or pace_sec > 59:
        return "Pace must be a valid time in minutes and seconds."

    # Validate slope
    if slope < 0 or slope > 100:
        return "Slope must be between 0 and 100%."

    # Validate strike pattern
    if not strike:
        return "Please select a strike pattern."

    # Validate headwind
    if headwind < -1 or headwind > 5:
        return "Headwind must be between -1 and 5 m/s."

    # Validate surface
    if not surface:
        return "Please select a surface."

    # If all inputs are valid, return None
    return None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/calc', methods=['POST'])
def calc():
    if request.method == 'POST':
        weight = int(request.form['weight']) # integer between 25 and 100
        gender = request.form['gender'] # string either M or F
        height = float(request.form['height']) # float up to 2 decimal places
        cadence = int(request.form['cadence']) # integer
        pace_min = int(request.form['pace_min']) # integer from 3 to 7
        pace_sec = int(request.form['pace_sec']) # integer from 0 to 59
        slope = float(request.form['slope']) # float given as percentage, 0.0 to 100.0
        strike = request.form['strike'] # string either RFS, FFS or MFS
        headwind = float(request.form['headwind']) # float between -1 and 5 m/s
        surface = request.form['surface'] # string either Road or trail

        validation_output = validate_inputs(weight, gender, height, cadence, pace_min, pace_sec, slope, strike, headwind, surface)
        if validation_output:
            return {"error": validation_output}

        run_sheet = xw.Book("Vimazi 2.0 walking running.xlsx").sheets[1]
        print(run_sheet.range('C5').value)

        # Change the values of the cells
        run_sheet.range('C5').value = weight
        run_sheet.range('C6').value = gender
        run_sheet.range('C7').value = height
        run_sheet.range('C8').value = cadence
        run_sheet.range('C9').value = strike
        run_sheet.range('C11').value = pace_min
        run_sheet.range('D11').value = pace_sec
        run_sheet.range('C12').value = slope
        run_sheet.range('C13').value = headwind
        run_sheet.range('C14').value = surface

        run_sheet.book.save()

        # Read the value from cell A1
        result = run_sheet.range('J10').value

        # Print the cell value
        print(result)

        # Close the workbook
        run_sheet.book.close()

        return {"result": result}
    abort(404, description="Invalid request")

if __name__ == '__main__':
    app.run(port=8000, debug=True)
