from PIL import Image
import numpy as np
from multiprocessing import Process, Queue
import time

def main():
    width = 1920
    hight = 1080
    start_x = -2.5
    stop_x = 1
    start_y = -1.2
    stop_y = 1.2
    max_iter = 5
    thread_count = 4
    output_path = "renders/{}.jpg"

    for i in range(5,100,5):
        print("sterted Process with max_iter: {}".format(i))
        output_array = mandelbrot_multiprocessing(hight,width,start_x,stop_x,start_y,stop_y,i,thread_count)

        output_image = Image.fromarray(np.uint8(output_array))
        output_image.save(output_path.format(i))

def mandelbrot_multiprocessing(hight,width,start_x,stop_x,start_y,stop_y,max_iter,thread_count):
    jobs = []
    result_queue = Queue()
    output_array = np.zeros([hight,width,3])

    with_slice_size = int(width/thread_count)
    x_slice_size = (stop_x-start_x)/thread_count
    for thread_number in range(thread_count):
        proc = Process(target=mandelbrot_process, args=(
            result_queue,
            with_slice_size*thread_number,
            hight,
            with_slice_size,
            start_x+x_slice_size*thread_number,
            start_x+x_slice_size*thread_number + x_slice_size,
            start_y,
            stop_y,
            max_iter))
        jobs.append(proc)
        proc.start()

    iter = 0
    while iter != thread_count:
        if not result_queue.empty():
            res = result_queue.get()
            for iy,ix in np.ndindex(res["result"].shape[:2]):
                output_array[iy][ix+res["x_offset"]] = res["result"][iy][ix]
            iter +=1
        else:
            time.sleep(0.1)

    return output_array

def mandelbrot_process(result_queue,x_offset,hight,width,start_x,stop_x,start_y,stop_y,max_iter):
    result_queue.put({
        "x_offset":x_offset,
        "result":mandelbrot(hight,width,start_x,stop_x,start_y,stop_y,max_iter)
    })

def mandelbrot(hight,width,start_x,stop_x,start_y,stop_y,max_iter):
    result = np.zeros([hight,width,3])
    for iy,ix in np.ndindex((hight,width)):
        scaled_x = scale(ix,(0,width),(start_x, stop_x))
        scaled_y = scale(iy,(0,hight),(start_y, stop_y))
        x = 0.0
        y = 0.0
        iteration = 0
        while x*x + y*y <= 2*2  and  iteration < max_iter:
            xtemp = x*x - y*y + scaled_x
            y = 2*x*y + scaled_y
            x = xtemp
            iteration = iteration + 1
        result[iy][ix] = color_gradiant(scale(iteration,(0,max_iter),(0,1)),max_iter)
    return result

def color_gradiant(iterations,max_iter):
    color_shema = [(0,0,0),(255,255,255)]
    mix = iterations
    c1 = np.array(color_shema[0])
    c2 = np.array(color_shema[1])
    res_color = mix*c1 + (1-mix)*c2
    return res_color

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

if __name__ == '__main__':
    main()
