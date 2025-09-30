"""Minimal HTTP server so the Meridian image is Cloud Run compatible."""

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os


class _HealthCheckHandler(BaseHTTPRequestHandler):
  """Responds with a short message confirming the service is running."""

  def do_GET(self):  # pylint: disable=invalid-name
    message = "Meridian service is running."
    body = message.encode("utf-8")

    self.send_response(HTTPStatus.OK)
    self.send_header("Content-Type", "text/plain; charset=utf-8")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def log_message(self, format, *args):  # pylint: disable=redefined-builtin
    # Silence the default request logging to keep Cloud Run logs cleaner.
    return


def main():
  port = int(os.environ.get("PORT", "8080"))
  server_address = ("", port)
  httpd = ThreadingHTTPServer(server_address, _HealthCheckHandler)
  httpd.serve_forever()


if __name__ == "__main__":
  main()
