#candy aigle noir
from datetime import datetime
from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():

    dict_rig = {}
    dict_rig_number = {2: "202",
                       3: "203",
                       4: "204"}
    
    for x,y, in dict_rig_number.items():
        try:
            response = requests.get("http://ripmundocrit.ddns.net:{0}/API.json".format(y), timeout=4)
            response_json = json.loads(response.text)
            uptime = response_json["results"]["avg_time"] * response_json["results"]["shares_good"]
            dict_rig[x] = dict()
            dict_rig[x].update({"hashrate": response_json["hashrate"]["total"][1]})
            dict_rig[x].update({"avg_time": response_json["results"]["avg_time"]})
            dict_rig[x].update({"uptime": "{0}:{1:0>2}:{2:0>2}".format(int(uptime//3600), int(uptime//60%60), int(uptime%60))})
        except requests.exceptions.RequestException:
            dict_rig[x] = dict()
            list_key = ["avg_time", "hashrate", "uptime"]
            for key in list_key:
                dict_rig[key].update({key: "rig down."})

    return render_template('hello.html', dict_rig=dict_rig)

if __name__ == '__main__':
    app.run(debug=True, port=1000, host='0.0.0.0', threaded=True)
