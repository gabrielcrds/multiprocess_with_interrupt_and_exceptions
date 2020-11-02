# multiprocess_with_interrupt_and_exceptions

Python 3 code to run multiprocess, stopping processes when a KeyboardInterrupt is sent or one of the processes triggers an exception.

This code has a main loop that will check for exceptions on processes every 5 seconds. KeyboardInterrupt should be caught instantly. 

### References:
- Inspired in this Python 2 code, adding some functionalities: [python-multiprocessing-keyboardinterrupt](https://noswap.com/blog/python-multiprocessing-keyboardinterrupt)
- Some stack overflow questions:
  - [exception-thrown-in-multiprocessing-pool-not-detected](https://stackoverflow.com/questions/6728236/exception-thrown-in-multiprocessing-pool-not-detected)
  - [keyboardinterrupts-with-pythons-multiprocessing-pool-imap](https://stackoverflow.com/questions/25783637/keyboardinterrupts-with-pythons-multiprocessing-pool-imap)
