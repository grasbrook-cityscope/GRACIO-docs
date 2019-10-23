import requests
import json
import urllib

def getCurrentState(fromwhere):
    with urllib.request.urlopen(fromwhere) as url:
        return json.loads(url.read().decode())
    return None

def read_json_file(settings_file):
        # open json file
        with open(settings_file) as d:
            data = json.load(d)
        return(data)

def send_json_to_cityIO(cityIO_json, name):
        # defining the api-endpoint
        post_address = "https://cityio.media.mit.edu/api/table/update/" + name

        r = requests.post(post_address, json=cityIO_json, headers={'Content-Type': 'application/json'})
        print(r)
        if not r.status_code == 200:
            print("could not post result to cityIO")
            print("Error code", r.status_code)
        else:
            print("Successfully posted to cityIO", r.status_code)


if __name__ == "__main__":
    data = read_json_file("sampletable.json")

    print(data["header"])

    send_json_to_cityIO(data,"grasbrook_test")


