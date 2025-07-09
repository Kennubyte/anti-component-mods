from flask import Flask, jsonify
import os
import time
import threading

app = Flask(__name__)

working_folder = r"C:\Users\jackd\AppData\Roaming\Stormworks\working_server\vehicles"

component_mods = {}

seen_files = set(os.listdir(working_folder))
for f in seen_files:
    if os.path.isdir(os.path.join(working_folder, f)):
        component_mods[f] = True

@app.route('/mods', methods=['GET'])
def get_mods():
    active_mods = [mod for mod, active in component_mods.items() if active]
    return jsonify(active_mods)

def watch_folder():
    global seen_files
    while True:
        time.sleep(2)
        current_files = set(os.listdir(working_folder))

        new_files = current_files - seen_files
        for nf in new_files:
            full_path = os.path.join(working_folder, nf)
            if os.path.isdir(full_path):
                component_mods[nf] = True
                print(f"WEEWOOO COMPONENT MOD ADDED: {nf}")

        removed_files = seen_files - current_files
        for rf in removed_files:
            if component_mods.get(rf):
                component_mods[rf] = False
                print(f"RIP COMPONENT MOD REMOVED: {rf}")

        seen_files = current_files

threading.Thread(target=watch_folder, daemon=True).start()

if __name__ == '__main__':
    app.run(port=6999)
