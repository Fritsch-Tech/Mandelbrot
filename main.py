from PIL import Image
import numpy as np
def main():
    size_x = 100
    size_y = 100
    start_x = -2.5
    stop_x = 1
    start_y = -1.2
    stop_y = 1.2
    max_iter = 100

    mandelbrot_array = mandelbrot(size_y,size_x,start_x,stop_x,start_y,stop_y,max_iter)
    mandelbrot_image = Image.fromarray(np.uint8(mandelbrot_array))
    mandelbrot_image.save("1.jpg")
    
def mandelbrot(size_y,size_x,start_x,stop_x,start_y,stop_y,max_iter):
    result = np.zeros([size_y,size_x,3])
    for iy,ix in np.ndindex((size_y,size_x)):
        scaled_x = scale(ix,(0,size_x),(start_x, stop_x))
        scaled_y = scale(iy,(0,size_y),(start_y, stop_y))
        x = 0.0
        y = 0.0
        iteration = 0
        while x*x + y*y <= 2*2  and  iteration < max_iter:
            xtemp = x*x - y*y + scaled_x
            y = 2*x*y + scaled_y
            x = xtemp
            iteration = iteration + 1
        result[iy][ix] = color_gradiant(scale(iteration,(0,max_iter),(0,1)))
    return result

def color_gradiant(iterations):
    return (scale(iterations,(0,1),(0,255)),
            scale(iterations,(0,1),(0,255)),
            scale(iterations,(0,1),(0,255)))

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

if __name__ == '__main__':
    main()
