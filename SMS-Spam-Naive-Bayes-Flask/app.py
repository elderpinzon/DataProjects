from flask import Flask,render_template,url_for,request
from sklearn.externals import joblib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    spam_pipeline = open('spam_pipeline.pkl','rb')
    clf = joblib.load(spam_pipeline)
    
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        prediction = clf.predict(data)
    
    return render_template('result.html', message=message, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
    predict()
