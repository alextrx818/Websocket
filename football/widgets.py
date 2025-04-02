from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Sports Alerts</title>
    </head>
    <body>
        <h1>Live Sports Alerts</h1>
        <div id="thesports_widget"></div>
        <script>
        (function (w, s, p, o, r, t) {
            r = document.createElement(s);
            t = document.getElementsByTagName(s)[0];
            r.async = true;
            r.src = p;
            t.parentNode.insertBefore(r, t);
            r.onload = () => {
                w["thesports"]?.setProfile(o.profile, o.options);
            };
        })(
            window,
            "script",
            `//cdn-saas.thesports.com/loader.umd.js?t=${parseInt(Date.now() / 1e7)}`,
            {
                profile: {
                    profile_id: "1234567890",  // Updated with actual profile ID
                    sport: "football",
                    widget_id: "match_overview",  // Updated with actual widget ID
                    competition_ids: ["comp123", "comp456"],  // Updated with actual competition IDs
                    lang: "en",
                },
                options: {},
            }
        );
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)