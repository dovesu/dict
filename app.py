from flask import(
    Flask, render_template, request, redirect, globals
)
import subprocess
app= Flask(__name__)
  
@app.route("/",methods=['GET', 'POST'])
def index():
     return render_template("index.html")
     
@app.route("/dict",methods=['GET', 'POST'])
def run():
    word = request.form.get('word')
    result = subprocess.Popen(['python','run.py',(word)], stdout=subprocess.PIPE)
    stderr = result.communicate()
    return stderr
if __name__ == '__main__':
    app.run(port=2020,host="0.0.0.0",debug=True)
