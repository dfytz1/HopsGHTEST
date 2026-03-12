from flask import Flask
import ghhops_server as hs
import rhino3dm as r3d

app = Flask(__name__)
hops = hs.Hops(app)


@hops.component(
    "/add",
    name="Add",
    description="Add two numbers",
    inputs=[hs.HopsNumber("A"), hs.HopsNumber("B")],
    outputs=[hs.HopsNumber("Sum")],
)
def add(a, b):
    return a + b


if __name__ == "__main__":
    app.run(debug=True)
