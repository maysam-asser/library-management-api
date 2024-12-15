import json
import uuid

class Database:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        with open(self.filename, 'r') as f:            
            return json.load(f)
   
    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

def generate_id():
    return str(uuid.uuid4().hex)