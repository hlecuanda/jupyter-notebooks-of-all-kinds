BIN=~/bin
OPTS=-o hector -g hector -p -m a+x,og-w -v
BINF!=basename calendarevents.py .py

.PHONY : install


install: calendarevents.py
	install $(opts) $? $(BIN)/$(BINF)
