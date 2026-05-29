import os
from http.server import BaseHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # URL query parse
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

            # validation
            if not phone and not user_id:
                response = {
                    "status": "error",
                    "message": "send phone or user_id"
                }

                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(str(response).encode())
                return

            # search all txt files
            for file_name in os.listdir(DATA_DIR):

                if not file_name.endswith(".txt"):
                    continue

                file_path = os.path.join(DATA_DIR, file_name)

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

                            # phone search
                            if phone and phone == file_phone:
                                response = {
                                    "status": "success",
                                    "result": line
                                }

                                self.send_response(200)
                                self.send_header("Content-type", "application/json")
                                self.end_headers()
                                self.wfile.write(str(response).encode())
                                return

                            # user id search
                            if user_id and user_id == file_user_id:
                                response = {
                                    "status": "success",
                                    "result": line
                                }

                                self.send_response(200)
                                self.send_header("Content-type", "application/json")
                                self.end_headers()
                                self.wfile.write(str(response).encode())
                                return

                except Exception:
                    continue

            # not found
            response = {
                "status": "error",
                "message": "not found"
            }

            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(str(response).encode())

        except Exception as e:
            response = {
                "status": "error",
                "message": str(e)
            }

            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(str(response).encode())
