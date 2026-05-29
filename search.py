import os
from http.server import BaseHTTPRequestHandler

BASE_DIR = os.path.dirname(__file__)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            path = self.path

            phone = None
            user_id = None

            if "?" in path:
                query = path.split("?", 1)[1]

                for item in query.split("&"):
                    if "=" in item:
                        key, value = item.split("=", 1)

                        if key == "phone":
                            phone = value.strip()

                        elif key == "user_id":
                            user_id = value.strip()

            if not phone and not user_id:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(
                    b'{"status":"error","message":"send phone or user_id"}'
                )
                return

            # current folder এর সব txt file search
            for file_name in os.listdir(BASE_DIR):

                if not file_name.endswith(".txt"):
                    continue

                file_path = os.path.join(BASE_DIR, file_name)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()

                            if not line:
                                continue

                            parts = line.split(":")

                            if len(parts) < 2:
                                continue

                            file_phone = parts[0]
                            file_user_id = parts[1]

                            if phone and phone == file_phone:
                                result = (
                                    '{"status":"success","result":"'
                                    + line.replace('"', '\\"')
                                    + '"}'
                                )

                                self.send_response(200)
                                self.send_header(
                                    "Content-type",
                                    "application/json"
                                )
                                self.end_headers()
                                self.wfile.write(result.encode())
                                return

                            if user_id and user_id == file_user_id:
                                result = (
                                    '{"status":"success","result":"'
                                    + line.replace('"', '\\"')
                                    + '"}'
                                )

                                self.send_response(200)
                                self.send_header(
                                    "Content-type",
                                    "application/json"
                                )
                                self.end_headers()
                                self.wfile.write(result.encode())
                                return

                except Exception:
                    continue

            self.send_response(404)
            self.end_headers()
            self.wfile.write(
                b'{"status":"error","message":"not found"}'
            )

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(
                f'{{"status":"error","message":"{str(e)}"}}'.encode()
            )
