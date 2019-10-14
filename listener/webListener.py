from websocket import create_connection
import json

class webListener:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, port):
        self.ws = create_connection('ws://127.0.0.1:{}'.format(port))
        self.dictPath = []
        self.curEventMsg = None

    def start_suite(self, name, attrs):       
        data = {
            'name': name,
            'type': 'Suite',
            'path': '.'.join(self.dictPath)
        }
        self.ws.send(json.dumps(data))
        self.dictPath.append('0')

    def end_suite(self, name, attrs):
        data = {
            'type': 'suite',
            'status': attrs['status']
        }
        self.ws.send(json.dumps(data))
        if len(self.dictPath) > 1:
            self.dictPath.pop()
            self.dictPath[-1] = str(int(self.dictPath[-1]) + 1)

    def start_test(self, name, attrs):
        data = {
            'name': name,
            'type': 'Test',
            'path': '.'.join(self.dictPath)
        }
        self.ws.send(json.dumps(data))
        self.dictPath.append('0')

    def end_test(self, name, attrs):
        data = {
            'type': 'test',
            'status': attrs['status']
        }
        self.ws.send(json.dumps(data))
        if self.dictPath:
            self.dictPath.pop()
            self.dictPath[-1] = str(int(self.dictPath[-1]) + 1)
    
    def start_keyword(self, name, attrs):
        if attrs['kwname'] != 'Capture Page Screenshot':
            data = {
                'name': attrs['kwname'],
                'type': 'Keyword',
                'path': '.'.join(self.dictPath)
            }
            if attrs['type'] == 'Setup':
                data['type'] = 'Setup'
            elif attrs['type'] == 'Teardown':
                data['type'] = 'Teardown'

            self.ws.send(json.dumps(data))
            self.dictPath.append('0')

    def end_keyword(self, name, attrs):
        if attrs['kwname'] != 'Capture Page Screenshot':
            data = {
                'type': 'keyword',
                'status': attrs['status'],
                'message': self.curEventMsg if attrs['status'] == 'FAIL' else None
            }
            self.ws.send(json.dumps(data))
            if self.dictPath:
                self.dictPath.pop()
                self.dictPath[-1] = str(int(self.dictPath[-1]) + 1)

    def log_message(self, attrs):
        self.curEventMsg = attrs['message']
