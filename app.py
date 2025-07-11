from flask import Flask,request,render_template,send_file
import qrcode
import io
import re
import base64

app = Flask(__name__)

def is_valid_url(url):
    pattern = re.compile(
        r'^(https?://)?'
        r'([\da-z\.-]+)\.([a-z\.]{2,6})'
        r'([/\w \.-]*)*/?$'
    )
    return re.match(pattern,url)

@app.route('/', methods = ['GET','POST'])
def index():
    error = ''
    url = ''
    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        if not url:
            error = 'URL is required'
        elif not is_valid_url(url):
            error = 'Invalid URL format'
        else:
            img = qrcode.make(url)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return send_file(
                buf,
                mimetype='image/png',
                as_attachment=True,
                download_name='qrcode.png'
            )
        
    return render_template('text.html', error = error, url = url)

if __name__ == '__main__':
    app.run(debug=True)