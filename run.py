import multiprocessing
import signal
import time

stop_processes = False
process_exception = None
n_processes_running = 0
global_lock = multiprocessing.Lock()

def init_process():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def run_process(i, error_on):
    time.sleep(i)
    if i == error_on:
        raise FileNotFoundError
    print(i, "seconds - done")


def signal_done(r):
    global global_logk, n_processes_running
    with global_lock:
        n_processes_running -= 1


def signal_stop(e):
    global stop_processes, process_exception
    stop_processes = True
    process_exception = e


def foo(error_on=-1):
    global stop_processes, process_exception, n_processes_running, global_lock

    print("Init processes")
    pool = multiprocessing.Pool(
        processes=3,
        initializer=init_process,
    )

    print("Starting 3 jobs.")
    for i in range(1, 4):
        with global_lock:
            n_processes_running += 1

        pool.apply_async(
            func=run_process,
            args=(i * 5, error_on),
            callback=signal_done,
            error_callback=signal_stop,
        )

    try:
        while True:
            with global_lock:
                if n_processes_running == 0:
                    break

            time.sleep(5)
            if stop_processes:
                raise process_exception

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
        print("Quitting normally")
        pool.close()
        pool.join()


if __name__ == "__main__":
    print("Running first test. Should terminate without errors...")
    foo()
    
    print(
        "\nRunning second test.",
        "Should raise an exception after aprox 10 seconds."
    )
    foo(error_on=10)