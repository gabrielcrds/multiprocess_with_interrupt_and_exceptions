import multiprocessing
import signal
import time

stop = False
exception = None

def init_process():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def run_process(i):
    time.sleep(i)
    print(i, "done")
    if i == 10:
        raise FileNotFoundError


def signal_stop(e):
    global stop, exception
    stop = True
    exception = e


def foo():
    print("Init workers")
    pool = multiprocessing.Pool(
        processes=3,
        initializer=init_process
    )

    print("Starting 3 jobs. The second should raise an exception")
    for i in range(1, 4):
        pool.apply_async(
            func=run_process,
            args=(i * 5, ),
            error_callback=signal_stop,
        )

    try:
        global stop, exception
        while True:
            time.sleep(5)
            if stop:
                raise exception

    except KeyboardInterrupt:
        print("KeyboardInterrupt, terminating processes...")
        pool.terminate()
        pool.join()

    except Exception as e:
        print("A process failed, terminating processes...")
        pool.terminate()
        pool.join()
        raise e   

    else:
        # As it is, it should never reach here.
        # To check this behavior, comment the if in run_processes
        print("Quitting normally")
        pool.close()
        pool.join()


if __name__ == "__main__":
    foo()