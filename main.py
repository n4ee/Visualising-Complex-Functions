import numpy as np
import PIL.Image as Image

from matplotlib.colors import hsv_to_rgb

def user_input():
    bounds_input = input("Enter the bounds for the complex plane (default is 10): ")
    bounds = float(bounds_input) if bounds_input else 10.0

    res_input = input("Enter the resolution for the complex plane (default is 1000): ")
    resolution = int(res_input) if res_input else 1000

    equation = input("Enter any equation (in terms of z): ")

    return bounds, resolution, equation

def create_complex_grid(bounds, resolution):
    xs = np.linspace(-bounds, bounds, resolution)
    ys = np.linspace(bounds, -bounds, resolution)
    X, Y = np.meshgrid(xs, ys)
    return X + (1j * Y)

def evaluate_equation(equation, Z):
    allowed_math = {
        "z": Z,
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
        "abs": np.abs,
        "pi": np.pi,
        "e": np.e,
        "j": 1j,
        "i": 1j
    }

    with np.errstate(all='ignore'):
        return eval(equation, {"__builtins__": {}}, allowed_math)

def render_image(W):
    # convert magnitude array into a value array
    r = np.abs(W)
    val = r / (1 + r)
    sat = 1 - val**50
    hue = (np.angle(W)) / (2 * np.pi) % 1

    # convert HSV values to RGB
    rgb = hsv_to_rgb(np.stack([hue, sat, val], axis=-1))
    rgb = (rgb * 255).astype(np.uint8)

    img = Image.fromarray(rgb)
    img.save("complex_plane.png")
    print("Image saved as complex_plane.png!")

def main():
    bounds, resolution, equation = user_input()
    Z = create_complex_grid(bounds, resolution)
    W = evaluate_equation(equation, Z)
    render_image(W)

if __name__ == "__main__":
    main()