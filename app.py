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
        num1 = int(request.form['arg1'])
        num2 = int(request.form['arg2'])
        num3 = int(request.form['arg3'])

        sheet = xw.Book("workbook.xlsx").sheets[0]

        # Change the values of a range of cells
        sheet.range('A1:A3').value = [[num1], [num2], [num3]]

        sheet.book.save()

        # Read the value from cell A1
        result = sheet.range('A5').value

        # Print the cell value
        print(result)

        # Close the workbook
        sheet.book.close()

        return {"result": result}
    abort(404, description="Invalid request")

if __name__ == '__main__':
    app.run(port=8000, debug=True)
