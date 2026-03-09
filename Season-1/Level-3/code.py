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

    def _open_safe(self, path):
        """Validates path against traversal attacks and opens the file safely."""
        if not path:
            return None, None

        base_dir = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

        if os.path.isabs(path):
            fullpath = os.path.realpath(path)
        else:
            normalized = os.path.normpath(path)
            seps = os.sep
            if os.altsep:
                seps += os.altsep
            normalized = normalized.lstrip(seps)
            fullpath = os.path.realpath(os.path.join(base_dir, normalized))

        if not fullpath.startswith(base_dir + os.sep):
            return None, None

        if not os.path.isfile(fullpath):
            return None, None

        with open(fullpath, 'rb') as f:
            data = bytearray(f.read())
        return fullpath, data

    # returns the path of an optional profile picture that users can set
    def get_prof_picture(self, path=None):
        # setting a profile picture is optional
        if not path:
            pass

        prof_picture_path, picture = self._open_safe(path)
        if not prof_picture_path:
            return None

        # assume that image is returned on screen after this
        return prof_picture_path

    # returns the path of an attached tax form that every user should submit
    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Error: Tax form is required for all users")

        safe, tax_data = self._open_safe(path)
        if not safe:
            return None

        # assume that tax data is returned on screen after this
        return safe
