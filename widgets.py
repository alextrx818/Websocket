from flask import Flask

app = Flask(__name__)

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
                    profile_id: "##########",  // Replace with your profile ID
                    sport: "football",
                    widget_id: "horizontal_fixtures",  // Replace with your widget ID
                    competition_ids: ["####", "####"],  // Replace with competition IDs
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