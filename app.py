from flask import Flask
import ghhops_server as hs
import rhino3dm as r3d

app = Flask(__name__)
hops = hs.Hops(app)


def _is_curve(obj):
    """True if obj looks like a rhino3dm curve (has PointAt)."""
    return obj is not None and hasattr(obj, "PointAt") and callable(getattr(obj, "PointAt"))


def _flatten_curves(obj):
    """Flatten Grasshopper tree/list into a single list of curve-like items."""
    out = []
    if obj is None:
        return out
    if isinstance(obj, list):
        for item in obj:
            out.extend(_flatten_curves(item))
        return out
    if _is_curve(obj):
        return [obj]
    return out


@hops.component(
    "/loft",
    name="Loft",
    description="Loft between curves (ruled surfaces between consecutive curves)",
    inputs=[
        hs.HopsCurve("Curves", "Crv", "Curves to loft in order", hs.HopsParamAccess.LIST),
    ],
    outputs=[
        hs.HopsSurface("Surfaces", "Srf", "Loft surfaces between consecutive curves", hs.HopsParamAccess.LIST),
    ],
)
def loft(curves):
    flat = _flatten_curves(curves)
    if not flat or len(flat) < 2:
        return []

    surfaces = []
    for i in range(len(flat) - 1):
        c0, c1 = flat[i], flat[i + 1]
        try:
            srf = r3d.NurbsSurface.CreateRuledSurface(c0, c1)
            if srf is not None:
                surfaces.append(srf)
        except Exception:
            continue

    return surfaces


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
