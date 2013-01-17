import os
import urllib, json, traceback
from functools import wraps
from flask import Flask, redirect, request, current_app, jsonify
from howdoi import howdoi

app = Flask(__name__)

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function

@app.route('/howdoi', methods=['GET','POST'])
@support_jsonp
def hello():
    try:
        query = urllib.quote_plus(request.args.get('q'))
        result = howdoi.get_instructions({'query': query})
    except Exception as e:
        print traceback.format_exc()
        return jsonify({'status':'error','msg': e.args ,'traceball':traceback.format_exc()})

    return jsonify({'status':'success','data': result})


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)