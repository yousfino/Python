# Description

The goal from this simple program is to familiarize myself with multi-threading.

This program defines two worker functions 'worker1' and 'worker2', each of which 
performs a simple counting task. The main program creates two threads, 't1' and 
't2', to run these worker functions. The 'start' method is called on both threads 
to start them running simultaneously. The 'join' method is called to wait for 
both threads to finish before the main program continues. The program output shows 
that both worker functions are running at the same time and that they are 
interleaved, with the order of their output alternating between worker 1 and worker 2.
