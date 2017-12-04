# cyhy-mailer :postal_horn: :mailbox: #

[![Build Status](https://travis-ci.org/jsf9k/cyhy-mailer.svg?branch=master)](https://travis-ci.org/jsf9k/cyhy-mailer)
[![Coverage Status](https://coveralls.io/repos/github/jsf9k/cyhy-mailer/badge.svg?branch=master)](https://coveralls.io/github/jsf9k/cyhy-mailer?branch=master)

`cyhy-mailer` is a tool for emailing Cyber Hygiene, `https-scan`, and
`trustymail` reports to the appropriate technical or distribution
e-mail addresses.

## Installation ##

After using `git` to clone the repository, you can install
`cyhy-mailer` using `pip`:
```bash
pip install /path/to/cyhy-mailer
```

## Usage ##

```bash
Usage:
  cyhy-mailer [options]
  cyhy-mailer (--cyhy-report-dir=DIRECTORY) (--financial-year=YEAR) (--fy-quarter=QUARTER) [--mail-server=SERVER] [--mail-port=PORT] [--db-creds-file=FILENAME] [--debug]
  cyhy-mailer (-h | --help)

Options:
  -h --help                   Show this message.
  --cyhy-report-dir=DIRECTORY The directory where the CYHY PDF reports are
                              located.
  -y --financial-year=YEAR    The four-digit financial year to which the
                              reports being mailed out correspond.
  -q --fy-quarter=QUARTER     The quarter of the financial year to which the
                              reports being mailed out correspond.  Expected
                              values are 1, 2, 3, or 4.
  -m --mail-server=SERVER     The hostname or IP address of the mail server
                              that should send the messages.
                              [default: smtp01.ncats.dhs.gov]
  -p --mail-port=PORT         The port to use when connecting to the mail
                              server that should send the messages.
                              [default: 25]
  -c --db-creds-file=FILENAME A YAML file containing the CYHY database
                              credentials.
                              [default: /run/secrets/database_creds.yml]
  -d --debug                  A Boolean value indicating whether the output
                              should include debugging messages or not.
```

## License ##

This project is in the worldwide [public domain](LICENSE.md).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
