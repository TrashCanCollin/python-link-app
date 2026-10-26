
from flask import Flask, request, redirect, render_template_string
from datetime import datetime
from secrets import token_urlsafe

app = Flask(__name__)

links = {}

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Link Redirect</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 80px;">
    <h2>You're about to visit another website</h2>
    <p>This link records click activity.</p>
    <a href="{{ destination }}">Continue to destination</a>
</body>
</html>
"""


@app.route("/create", methods=["GET", "POST"])
def create_link():
    if request.method == "POST":
        destination = request.form.get("url", "").strip()

        if not destination.startswith(("https://", "http://")):
            return "Enter a valid HTTP or HTTPS URL.", 400

        code = token_urlsafe(6)
        links[code] = destination

        short_url = request.host_url + code

        print(f"[{datetime.now()}] Link created: {short_url}")
        print(f"Destination: {destination}")

        return f"Your link: <a href='{short_url}'>{short_url}</a>"

    return """
    <h2>Create a short link</h2>
    <form method="post">
        <input name="url" type="url"
               placeholder="https://example.com" required>
        <button type="submit">Create link</button>
    </form>
    """


@app.route("/<code>")
def visit_link(code):
    destination = links.get(code)

    if not destination:
        return "Link not found or server restarted.", 404

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log click activity without collecting visitor IP addresses.
    print(f"[{timestamp}] Link clicked: {code}")
    print(f"Redirecting to: {destination}")

    return render_template_string(PAGE, destination=destination)


if __name__ == "__main__":
    print("Link logger running at http://127.0.0.1:5000/create")
    app.run(host="127.0.0.1", port=5000, debug=False)
