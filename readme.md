# ts

`ts` is a simple CLI for tracking how long you spend on tasks-- its name stands for "timesheet".  Name those tasks with consistent tags, such as `coding` or `cleaning`, and you'll be able to track them over time.  You can answer questions like:

* Where does my time go on an average day?
* Did I study Japanese each day last week?
* How much time did I spend exercising?
* I'm pretty sure I only watched Netflix for an hour last night...is that true?

## future work
### analysis
There's lots of easy queries I'll add.  I wonder if it's worth making a language-based query interface instead of a bunch of 1-off commands, e.g. `./ts query count_of <keyword> days 7` or `./ts query time_spent <keyword>`.


### interface
One could build a frontend on top of this.  We can easily make a local Python server and interface using a browser.  If we were really cool we'd make an app, but no, that's ok.