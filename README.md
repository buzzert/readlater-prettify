# Read Later Prettify Sieve Script

I use this script as a way to cache a web page for reading later via email using sieve's [Extprograms](https://doc.dovecot.org/configuration_manual/sieve/plugins/extprograms/) plugin. 

It downloads the page via `urllib` and formats (prettifies) it via `BeautifulSoup`. 

## Installation
1. Make sure the sieve and Extprograms plugins are enabled on Dovecot. It is usually enabled by default. 
2. Edit your sieve-extprograms.conf to specify where to find the filter program:

/etc/dovecot/conf.d/90-sieve-extprograms.conf: 
```aconf
plugin {
  sieve_extensions = +vnd.dovecot.filter

  # The directory where the program sockets are located for the
  # vnd.dovecot.pipe, vnd.dovecot.filter and vnd.dovecot.execute extension
  # respectively. The name of each unix socket contained in that directory
  # directly maps to a program-name referenced from the Sieve script.
  sieve_pipe_socket_dir = sieve-pipe
  sieve_filter_socket_dir = sieve-filter
  sieve_execute_socket_dir = sieve-execute

  # The directory where the scripts are located for direct execution by the
  # vnd.dovecot.pipe, vnd.dovecot.filter and vnd.dovecot.execute extension
  # respectively. The name of each script contained in that directory
  # directly maps to a program-name referenced from the Sieve script.
  sieve_pipe_bin_dir = /usr/lib/dovecot/sieve-pipe
  sieve_filter_bin_dir = /usr/lib/dovecot/sieve-filter
  sieve_execute_bin_dir = /usr/lib/dovecot/sieve-execute
}
```

3. Copy this script (prettify.py) to the location specified above (i.e., /usr/lib/dovecot/sieve-filter). 
4. Add a line to your sieve file for when you want to execute this program. For example, I have it so when I send an email to "read@{my email.com}", it pipes the message into my program. The output is used for the message that is finally saved to the mailbox. This also files it into a special mailbox called "Read Later"
```sieve
# Read Later
if address :is "to" "read@{my email.com}" {
    filter "prettify.py";
    fileinto :create "Read Later";
}
```
5. Compile sieve with `sievec {sieve location}`
6. Restart dovecot


