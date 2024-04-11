from flask import Flask, request, abort, render_template
import xlwings as xw

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/calc', methods=['POST'])
def calc():
    error = None
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

        run_sheet = xw.Book("Vimazi 2.0 walking running.xlsx").sheets[1]
        print(run_sheet.range('C5').value)

        # Change the values of the cells
        run_sheet.range('C5').value = weight
        # run_sheet.range('C6').value = gender
        # run_sheet.range('C7').value = height
        # run_sheet.range('C8').value = cadence
        # run_sheet.range('C9').value = strike
        # run_sheet.range('C11').value = pace_min
        # run_sheet.range('D11').value = pace_sec
        # run_sheet.range('C12').value = slope
        # run_sheet.range('C13').value = headwind
        # run_sheet.range('C14').value = surface

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
