import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug import secure_filename
import uuid, subprocess
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
CORS(app)

@app.route('/', methods=['POST'])
def convert_mapinfo_geojson():
    if request.method == 'POST':
        status = ""
        detail = ""
        uploadFile = request.files.getlist("mapinfofile")
        temp_filename = uuid.uuid4().hex
        temp_filebucket = []
        for _file in uploadFile:
            _ , extension = os.path.splitext(secure_filename(_file.filename))
            _file.save(temp_filename + extension)
            temp_filebucket.append(temp_filename + extension)

        command = "ogr2ogr -f GeoJSON \"%s.geojson\" \"%s.TAB\""%(temp_filename, temp_filename)
        try:
            print "Running command :", command
            subprocess.check_output(command)
            with open(temp_filename+".geojson",'r') as geojson:
                detail = json.load(geojson)
                print detail
            temp_filebucket.append(temp_filename + ".geojson")
            status = "OK"
        except:
            status = "ERROR"
            print "Error convert from mapinfo to geojson"
            detail = "Error convert from mapinfo to geojson"
            
        for _file in temp_filebucket:
            os.remove(_file)

        return jsonify({"status":status,"detail":detail})
    else:
        return jsonify({"status":"ERROR", "detail":"Invalid request"})

if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))