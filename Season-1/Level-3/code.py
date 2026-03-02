# Welcome to Secure Code Game Season-1/Level-3!

# You know how to play by now, good luck!

import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    def _safe_path(self, path):
        if not path:
            return None

        base_dir = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

        # Reject absolute paths outright
        if os.path.isabs(path):
            return None

        # Normalize the user-supplied path and remove any leading separators
        normalized_path = os.path.normpath(path).lstrip(os.sep)

        # Build the full path and resolve it to a real path
        filepath = os.path.realpath(os.path.join(base_dir, normalized_path))

        # Ensure the final path is strictly within base_dir
        common = os.path.commonpath([base_dir, filepath])
        if common != base_dir or filepath == base_dir:
            return None

        return filepath

    # returns the path of an optional profile picture that users can set
    def get_prof_picture(self, path=None):
        # setting a profile picture is optional
        if not path:
            pass

        # defends against path traversal attacks
        prof_picture_path = self._safe_path(path)
        if not prof_picture_path:
            return None

        with open(prof_picture_path, 'rb') as pic:
            picture = bytearray(pic.read())

        # assume that image is returned on screen after this
        return prof_picture_path

    # returns the path of an attached tax form that every user should submit
    def get_tax_form_attachment(self, path=None):
        tax_data = None

        if not path:
            raise Exception("Error: Tax form is required for all users")

        # defends against path traversal attacks
        safe = self._safe_path(path)
        if not safe:
            return None

        with open(safe, 'rb') as form:
            tax_data = bytearray(form.read())

        # assume that tax data is returned on screen after this
        return safe