# Embedded C Code Analysis

## What the Code Does

This program controls a motor on a microcontroller. It waits for a timer, checks if a button was pressed, and updates a control register to drive the motor. If the timer fires without a button press, the register is cleared to zero, stopping the motor.

## Identified Problems

- **Missing `volatile`** — the timer and button flags can be cached by the compiler, causing the program to freeze in an infinite loop
- **Wasted CPU time** — the processor does nothing but wait in a loop until the timer fires instead of doing useful work
- **Unpredictable register values** — if the timer and button trigger at the exact same time, the register can end up with an unintended value
- **Register corruption** — the register can be written from two places at once, causing its value to be overwritten unexpectedly
