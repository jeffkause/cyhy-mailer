"""This module contains the tests for the HttpsMessage class."""

# Standard Python Libraries
import unittest

# cisagov Libraries
from cyhy.mailer.HttpsMessage import HttpsMessage


class Test(unittest.TestCase):
    """The tests for the HttpsMessage class."""

    def test_four_params_single_recipient(self):
        """Test the 4-parameter version of the constructor."""
        to = ["recipient@example.com"]
        pdf = "./tests/data/pdf-sample.pdf"
        entity_acronym = "CLARKE"
        entity_name = "Clarke of Kent"
        report_date = "December 15, 2001"

        message = HttpsMessage(to, pdf, entity_acronym, entity_name, report_date)

        self.assertEqual(message["From"], "reports@cyber.dhs.gov")
        self.assertEqual(
            message["Subject"], "CLARKE - HTTPS Report - December 15, 2001 Results"
        )
        self.assertEqual(message.get("CC"), None)
        self.assertEqual(message["BCC"], "cyhy_reports@hq.dhs.gov")
        self.assertEqual(message["To"], "recipient@example.com")

        # Grab the bytes that comprise the attachment
        bytes = open(pdf, "rb").read()

        # Make sure the correct body and PDF attachments were added
        for part in message.walk():
            # multipart/* are just containers
            if part.get_content_type() == "application/pdf":
                self.assertEqual(part.get_payload(decode=True), bytes)
                self.assertEqual(part.get_filename(), "pdf-sample.pdf")
            elif part.get_content_type() == "text/plain":
                text_body = """Greetings Clarke of Kent (CLARKE),

Attached is your latest HTTPS Report.

This report is intended to assist your agency in complying with OMB M-15-13 and CISA Binding Operational Directive 18-01.

This report includes all second-level .gov domains your agency owns and many known subdomains. Subdomains are gleaned from Cyber Hygiene scans, the General Services Administration's Digital Analytics Program, Censys.io, and data from the End of Term Web Archive. The data in this report comes from a scan that took place on December 15, 2001.

The embedded CSV, pshtt-results.csv, contains the raw scores for compliance. For domains where "Live" == "True", when "Domain Supports HTTPS", "Domain Enforces HTTPS", and "Domain Uses Strong HSTS" are all "True", OR where "HSTS Base Domain Preloaded" is "True", that domain is M-15-13 compliant. Domains where "Live" == "False" are not web-responsive and do not fall under M-15-13's scope.

We welcome your feedback and questions.

Cheers,
CISA Cyber Assessments - Cyber Hygiene
Cybersecurity and Infrastructure Security Agency
vulnerability@cisa.dhs.gov

----changelog----
03/28/2017
* Fixed: Compliance scores in the "Executive Summary" now account for preloaded domains. Preloading is OMB's preferred method for HSTS compliance.

02/15/2017
* Fixed an issue where some hostnames would appear twice in pshtt-results.csv
* Fixed: A local caching error caused domains that have been HSTS preloaded after December 19th, 2016 to be reported incorrectly
* Known issue: Compliance scores in the "Executive Summary" section are not yet accounting for preloaded domains

01/25/2017
* Fixed: A flaw in the report logic would sometimes cause the "Results" section of the PDF to inaccurately represent raw pshtt scores. This error would also represent domains that were "HSTS Preload Ready" or "HSTS Preload Pending" as preloaded (a checkmark).
* Added: The report will now represent domains with "bad chain" errors (but not hostname or expired certificate errors) that otherwise satisfy M-15-13 as compliant. This is in line with M-15-13 not requiring the use of a particular certificate authority
--------------------
"""
                self.assertEqual(part.get_payload(), text_body)
            elif part.get_content_type() == "text/html":
                html_body = """<html>
<head></head>
<body>
<div style=""font-size:14.5"">
<p>Greetings Clarke of Kent (CLARKE),</p>
<p>Attached is your latest HTTPS Report.</p>
<p>This report is intended to assist your agency in complying with OMB <a href="https://https.cio.gov">M-15-13</a> and CISA <a href="https://cyber.dhs.gov/bod/18-01/">Binding Operational Directive 18-01</a>.</p>
<p>This report includes all second-level .gov domains your agency owns and many known subdomains. Subdomains are gleaned from Cyber Hygiene scans, the General Services Administration's <a href="https://analytics.usa.gov/">Digital Analytics Program</a>, <a href=https://censys.io>Censys.io</a>, and data from the <a href="http://eotarchive.cdlib.org/">End of Term Web Archive</a>. The data in this report comes from a <b>scan that took place on December 15, 2001.</b></p>
<p>The embedded CSV, pshtt-results.csv, contains the raw scores for compliance. <i>For domains where &ldquo;Live&rdquo; == &ldquo;True&rdquo;</i>, when &ldquo;Domain Supports HTTPS&rdquo;, &ldquo;Domain Enforces HTTPS&rdquo;, and &ldquo;Domain Uses Strong HSTS&rdquo; are all &ldquo;True&rdquo;, OR where &ldquo;HSTS Base Domain Preloaded&rdquo; is &ldquo;True&rdquo;, that domain is M-15-13 compliant. Domains where &ldquo;Live&rdquo; == &ldquo;False&rdquo; are not web-responsive and do not fall under M-15-13's scope.</p>
<p>We welcome your feedback and questions.</p>
<p>Cheers,<br>
CISA Cyber Assessments - Cyber Hygiene<br><br />
Cybersecurity and Infrastructure Security Agency<br />
<a href=""mailto:vulnerability@cisa.dhs.gov""> vulnerability@cisa.dhs.gov </a>
</p>
</div>
</p><br>
<p>----changelog----</p>
<p><i>03/28/2017</i></p>
<p><b>* Fixed:</b> Compliance scores in the &ldquo;Executive Summary&rdquo; now account for preloaded domains. Preloading is OMB's <a href="https://https.cio.gov/guide/#options-for-hsts-compliance">preferred method</a> for HSTS compliance.</p></p>
<p><i>02/15/2017</i></p>
<p><b>* Fixed</b> an issue where some hostnames would appear twice in<b> pshtt-results.csv <br>
* Fixed: </b>A local caching error caused domains that have been HSTS preloaded after December 19th, 2016 to be reported incorrectly<br>
<b>* Known issue</b>: Compliance scores in the &ldquo;Executive Summary&rdquo; section are not yet accounting for preloaded domains</p>
<p><i>01/25/2017</i></p>
<p><b>* Fixed</b>: A flaw in the report logic would sometimes cause the &ldquo;Results&rdquo; section of the PDF to inaccurately represent raw pshtt scores. This error would also represent domains that were &ldquo;HSTS Preload Ready&rdquo; or &ldquo;HSTS Preload Pending&rdquo; as preloaded (a checkmark).<br>
<b>* Added</b>: The report will now represent domains with &ldquo;bad chain&rdquo; errors (but not hostname or expired certificate errors) that otherwise satisfy M-15-13 as compliant. This is in line with M-15-13 <a href="https://https.cio.gov/certificates/#are-there-federal-restrictions-on-acceptable-certificate-authorities-to-use%3f">not requiring the use of a particular certificate authority</a>.</p>
<p>--------------------</p>
</body>
</html>
"""
                self.assertEqual(part.get_payload(), html_body)

    def test_four_params_multiple_recipients(self):
        """Test the 4-parameter version of the constructor."""
        to = ["recipient@example.com", "recipient2@example.com"]
        pdf = "./tests/data/pdf-sample.pdf"
        entity_acronym = "CLARKE"
        entity_name = "Clarke of Kent"
        report_date = "December 15, 2001"

        message = HttpsMessage(to, pdf, entity_acronym, entity_name, report_date)

        self.assertEqual(message["From"], "reports@cyber.dhs.gov")
        self.assertEqual(
            message["Subject"], "CLARKE - HTTPS Report - December 15, 2001 Results"
        )
        self.assertEqual(message.get("CC"), None)
        self.assertEqual(message["BCC"], "cyhy_reports@hq.dhs.gov")
        self.assertEqual(message["To"], "recipient@example.com,recipient2@example.com")

        # Grab the bytes that comprise the attachment
        bytes = open(pdf, "rb").read()

        # Make sure the correct body and PDF attachments were added
        for part in message.walk():
            # multipart/* are just containers
            if part.get_content_type() == "application/pdf":
                self.assertEqual(part.get_payload(decode=True), bytes)
                self.assertEqual(part.get_filename(), "pdf-sample.pdf")
            elif part.get_content_type() == "text/plain":
                body = """Greetings Clarke of Kent (CLARKE),

Attached is your latest HTTPS Report.

This report is intended to assist your agency in complying with OMB M-15-13 and CISA Binding Operational Directive 18-01.

This report includes all second-level .gov domains your agency owns and many known subdomains. Subdomains are gleaned from Cyber Hygiene scans, the General Services Administration's Digital Analytics Program, Censys.io, and data from the End of Term Web Archive. The data in this report comes from a scan that took place on December 15, 2001.

The embedded CSV, pshtt-results.csv, contains the raw scores for compliance. For domains where "Live" == "True", when "Domain Supports HTTPS", "Domain Enforces HTTPS", and "Domain Uses Strong HSTS" are all "True", OR where "HSTS Base Domain Preloaded" is "True", that domain is M-15-13 compliant. Domains where "Live" == "False" are not web-responsive and do not fall under M-15-13's scope.

We welcome your feedback and questions.

Cheers,
CISA Cyber Assessments - Cyber Hygiene
Cybersecurity and Infrastructure Security Agency
vulnerability@cisa.dhs.gov

----changelog----
03/28/2017
* Fixed: Compliance scores in the "Executive Summary" now account for preloaded domains. Preloading is OMB's preferred method for HSTS compliance.

02/15/2017
* Fixed an issue where some hostnames would appear twice in pshtt-results.csv
* Fixed: A local caching error caused domains that have been HSTS preloaded after December 19th, 2016 to be reported incorrectly
* Known issue: Compliance scores in the "Executive Summary" section are not yet accounting for preloaded domains

01/25/2017
* Fixed: A flaw in the report logic would sometimes cause the "Results" section of the PDF to inaccurately represent raw pshtt scores. This error would also represent domains that were "HSTS Preload Ready" or "HSTS Preload Pending" as preloaded (a checkmark).
* Added: The report will now represent domains with "bad chain" errors (but not hostname or expired certificate errors) that otherwise satisfy M-15-13 as compliant. This is in line with M-15-13 not requiring the use of a particular certificate authority
--------------------
"""
                self.assertEqual(part.get_payload(), body)
            elif part.get_content_type() == "text/html":
                html_body = """<html>
<head></head>
<body>
<div style=""font-size:14.5"">
<p>Greetings Clarke of Kent (CLARKE),</p>
<p>Attached is your latest HTTPS Report.</p>
<p>This report is intended to assist your agency in complying with OMB <a href="https://https.cio.gov">M-15-13</a> and CISA <a href="https://cyber.dhs.gov/bod/18-01/">Binding Operational Directive 18-01</a>.</p>
<p>This report includes all second-level .gov domains your agency owns and many known subdomains. Subdomains are gleaned from Cyber Hygiene scans, the General Services Administration's <a href="https://analytics.usa.gov/">Digital Analytics Program</a>, <a href=https://censys.io>Censys.io</a>, and data from the <a href="http://eotarchive.cdlib.org/">End of Term Web Archive</a>. The data in this report comes from a <b>scan that took place on December 15, 2001.</b></p>
<p>The embedded CSV, pshtt-results.csv, contains the raw scores for compliance. <i>For domains where &ldquo;Live&rdquo; == &ldquo;True&rdquo;</i>, when &ldquo;Domain Supports HTTPS&rdquo;, &ldquo;Domain Enforces HTTPS&rdquo;, and &ldquo;Domain Uses Strong HSTS&rdquo; are all &ldquo;True&rdquo;, OR where &ldquo;HSTS Base Domain Preloaded&rdquo; is &ldquo;True&rdquo;, that domain is M-15-13 compliant. Domains where &ldquo;Live&rdquo; == &ldquo;False&rdquo; are not web-responsive and do not fall under M-15-13's scope.</p>
<p>We welcome your feedback and questions.</p>
<p>Cheers,<br>
CISA Cyber Assessments - Cyber Hygiene<br><br />
Cybersecurity and Infrastructure Security Agency<br />
<a href=""mailto:vulnerability@cisa.dhs.gov""> vulnerability@cisa.dhs.gov </a>
</p>
</div>
</p><br>
<p>----changelog----</p>
<p><i>03/28/2017</i></p>
<p><b>* Fixed:</b> Compliance scores in the &ldquo;Executive Summary&rdquo; now account for preloaded domains. Preloading is OMB's <a href="https://https.cio.gov/guide/#options-for-hsts-compliance">preferred method</a> for HSTS compliance.</p></p>
<p><i>02/15/2017</i></p>
<p><b>* Fixed</b> an issue where some hostnames would appear twice in<b> pshtt-results.csv <br>
* Fixed: </b>A local caching error caused domains that have been HSTS preloaded after December 19th, 2016 to be reported incorrectly<br>
<b>* Known issue</b>: Compliance scores in the &ldquo;Executive Summary&rdquo; section are not yet accounting for preloaded domains</p>
<p><i>01/25/2017</i></p>
<p><b>* Fixed</b>: A flaw in the report logic would sometimes cause the &ldquo;Results&rdquo; section of the PDF to inaccurately represent raw pshtt scores. This error would also represent domains that were &ldquo;HSTS Preload Ready&rdquo; or &ldquo;HSTS Preload Pending&rdquo; as preloaded (a checkmark).<br>
<b>* Added</b>: The report will now represent domains with &ldquo;bad chain&rdquo; errors (but not hostname or expired certificate errors) that otherwise satisfy M-15-13 as compliant. This is in line with M-15-13 <a href="https://https.cio.gov/certificates/#are-there-federal-restrictions-on-acceptable-certificate-authorities-to-use%3f">not requiring the use of a particular certificate authority</a>.</p>
<p>--------------------</p>
</body>
</html>
"""
                self.assertEqual(part.get_payload(), html_body)

    def test_six_params_single_cc(self):
        """Test the 6-parameter version of the constructor."""
        to = ["recipient@example.com", "recipient2@example.com"]
        pdf = "./tests/data/pdf-sample.pdf"
        fm = "sender@example.com"
        cc = ["cc@example.com"]
        bcc = ["bcc@example.com"]
        entity_acronym = "CLARKE"
        entity_name = "Clarke of Kent"
        report_date = "December 15, 2001"

        message = HttpsMessage(
            to,
            pdf,
            entity_acronym,
            entity_name,
            report_date,
            from_addr=fm,
            cc_addrs=cc,
            bcc_addrs=bcc,
        )

        self.assertEqual(message["From"], fm)
        self.assertEqual(
            message["Subject"], "CLARKE - HTTPS Report - December 15, 2001 Results"
        )
        self.assertEqual(message["CC"], "cc@example.com")
        self.assertEqual(message["BCC"], "bcc@example.com")
        self.assertEqual(message["To"], "recipient@example.com,recipient2@example.com")

        # Grab the bytes that comprise the attachment
        bytes = open(pdf, "rb").read()

        # Make sure the correct body and PDF attachments were added
        for part in message.walk():
            # multipart/* are just containers
            if part.get_content_type() == "application/pdf":
                self.assertEqual(part.get_payload(decode=True), bytes)
                self.assertEqual(part.get_filename(), "pdf-sample.pdf")
            elif part.get_content_type() == "text/plain":
                body = """Greetings Clarke of Kent (CLARKE),

Attached is your latest HTTPS Report.

This report is intended to assist your agency in complying with OMB M-15-13 and CISA Binding Operational Directive 18-01.

This report includes all second-level .gov domains your agency owns and many known subdomains. Subdomains are gleaned from Cyber Hygiene scans, the General Services Administration's Digital Analytics Program, Censys.io, and data from the End of Term Web Archive. The data in this report comes from a scan that took place on December 15, 2001.

The embedded CSV, pshtt-results.csv, contains the raw scores for compliance. For domains where "Live" == "True", when "Domain Supports HTTPS", "Domain Enforces HTTPS", and "Domain Uses Strong HSTS" are all "True", OR where "HSTS Base Domain Preloaded" is "True", that domain is M-15-13 compliant. Domains where "Live" == "False" are not web-responsive and do not fall under M-15-13's scope.

We welcome your feedback and questions.

Cheers,
CISA Cyber Assessments - Cyber Hygiene
Cybersecurity and Infrastructure Security Agency
vulnerability@cisa.dhs.gov

----changelog----
03/28/2017
* Fixed: Compliance scores in the "Executive Summary" now account for preloaded domains. Preloading is OMB's preferred method for HSTS compliance.

02/15/2017
* Fixed an issue where some hostnames would appear twice in pshtt-results.csv
* Fixed: A local caching error caused domains that have been HSTS preloaded after December 19th, 2016 to be reported incorrectly
* Known issue: Compliance scores in the "Executive Summary" section are not yet accounting for preloaded domains

01/25/2017
* Fixed: A flaw in the report logic would sometimes cause the "Results" section of the PDF to inaccurately represent raw pshtt scores. This error would also represent domains that were "HSTS Preload Ready" or "HSTS Preload Pending" as preloaded (a checkmark).
* Added: The report will now represent domains with "bad chain" errors (but not hostname or expired certificate errors) that otherwise satisfy M-15-13 as compliant. This is in line with M-15-13 not requiring the use of a particular certificate authority
--------------------
"""
                self.assertEqual(part.get_payload(), body)
            elif part.get_content_type() == "text/html":
                html_body = """<html>
<head></head>
<body>
<div style=""font-size:14.5"">
<p>Greetings Clarke of Kent (CLARKE),</p>
<p>Attached is your latest HTTPS Report.</p>
<p>This report is intended to assist your agency in complying with OMB <a href="https://https.cio.gov">M-15-13</a> and CISA <a href="https://cyber.dhs.gov/bod/18-01/">Binding Operational Directive 18-01</a>.</p>
<p>This report includes all second-level .gov domains your agency owns and many known subdomains. Subdomains are gleaned from Cyber Hygiene scans, the General Services Administration's <a href="https://analytics.usa.gov/">Digital Analytics Program</a>, <a href=https://censys.io>Censys.io</a>, and data from the <a href="http://eotarchive.cdlib.org/">End of Term Web Archive</a>. The data in this report comes from a <b>scan that took place on December 15, 2001.</b></p>
<p>The embedded CSV, pshtt-results.csv, contains the raw scores for compliance. <i>For domains where &ldquo;Live&rdquo; == &ldquo;True&rdquo;</i>, when &ldquo;Domain Supports HTTPS&rdquo;, &ldquo;Domain Enforces HTTPS&rdquo;, and &ldquo;Domain Uses Strong HSTS&rdquo; are all &ldquo;True&rdquo;, OR where &ldquo;HSTS Base Domain Preloaded&rdquo; is &ldquo;True&rdquo;, that domain is M-15-13 compliant. Domains where &ldquo;Live&rdquo; == &ldquo;False&rdquo; are not web-responsive and do not fall under M-15-13's scope.</p>
<p>We welcome your feedback and questions.</p>
<p>Cheers,<br>
CISA Cyber Assessments - Cyber Hygiene<br><br />
Cybersecurity and Infrastructure Security Agency<br />
<a href=""mailto:vulnerability@cisa.dhs.gov""> vulnerability@cisa.dhs.gov </a>
</p>
</div>
</p><br>
<p>----changelog----</p>
<p><i>03/28/2017</i></p>
<p><b>* Fixed:</b> Compliance scores in the &ldquo;Executive Summary&rdquo; now account for preloaded domains. Preloading is OMB's <a href="https://https.cio.gov/guide/#options-for-hsts-compliance">preferred method</a> for HSTS compliance.</p></p>
<p><i>02/15/2017</i></p>
<p><b>* Fixed</b> an issue where some hostnames would appear twice in<b> pshtt-results.csv <br>
* Fixed: </b>A local caching error caused domains that have been HSTS preloaded after December 19th, 2016 to be reported incorrectly<br>
<b>* Known issue</b>: Compliance scores in the &ldquo;Executive Summary&rdquo; section are not yet accounting for preloaded domains</p>
<p><i>01/25/2017</i></p>
<p><b>* Fixed</b>: A flaw in the report logic would sometimes cause the &ldquo;Results&rdquo; section of the PDF to inaccurately represent raw pshtt scores. This error would also represent domains that were &ldquo;HSTS Preload Ready&rdquo; or &ldquo;HSTS Preload Pending&rdquo; as preloaded (a checkmark).<br>
<b>* Added</b>: The report will now represent domains with &ldquo;bad chain&rdquo; errors (but not hostname or expired certificate errors) that otherwise satisfy M-15-13 as compliant. This is in line with M-15-13 <a href="https://https.cio.gov/certificates/#are-there-federal-restrictions-on-acceptable-certificate-authorities-to-use%3f">not requiring the use of a particular certificate authority</a>.</p>
<p>--------------------</p>
</body>
</html>
"""
                self.assertEqual(part.get_payload(), html_body)

    def test_six_params_multiple_cc(self):
        """Test the 6-parameter version of the constructor."""
        to = ["recipient@example.com", "recipient2@example.com"]
        pdf = "./tests/data/pdf-sample.pdf"
        fm = "sender@example.com"
        cc = ["cc@example.com", "cc2@example.com"]
        bcc = ["bcc@example.com", "bcc2@example.com"]
        entity_acronym = "CLARKE"
        entity_name = "Clarke of Kent"
        report_date = "December 15, 2001"

        message = HttpsMessage(
            to,
            pdf,
            entity_acronym,
            entity_name,
            report_date,
            from_addr=fm,
            cc_addrs=cc,
            bcc_addrs=bcc,
        )

        self.assertEqual(message["From"], fm)
        self.assertEqual(
            message["Subject"], "CLARKE - HTTPS Report - December 15, 2001 Results"
        )
        self.assertEqual(message["CC"], "cc@example.com,cc2@example.com")
        self.assertEqual(message["BCC"], "bcc@example.com,bcc2@example.com")
        self.assertEqual(message["To"], "recipient@example.com,recipient2@example.com")

        # Grab the bytes that comprise the attachment
        bytes = open(pdf, "rb").read()

        # Make sure the correct body and PDF attachments were added
        for part in message.walk():
            # multipart/* are just containers
            if part.get_content_type() == "application/pdf":
                self.assertEqual(part.get_payload(decode=True), bytes)
                self.assertEqual(part.get_filename(), "pdf-sample.pdf")
            elif part.get_content_type() == "text/plain":
                body = """Greetings Clarke of Kent (CLARKE),

Attached is your latest HTTPS Report.

This report is intended to assist your agency in complying with OMB M-15-13 and CISA Binding Operational Directive 18-01.

This report includes all second-level .gov domains your agency owns and many known subdomains. Subdomains are gleaned from Cyber Hygiene scans, the General Services Administration's Digital Analytics Program, Censys.io, and data from the End of Term Web Archive. The data in this report comes from a scan that took place on December 15, 2001.

The embedded CSV, pshtt-results.csv, contains the raw scores for compliance. For domains where "Live" == "True", when "Domain Supports HTTPS", "Domain Enforces HTTPS", and "Domain Uses Strong HSTS" are all "True", OR where "HSTS Base Domain Preloaded" is "True", that domain is M-15-13 compliant. Domains where "Live" == "False" are not web-responsive and do not fall under M-15-13's scope.

We welcome your feedback and questions.

Cheers,
CISA Cyber Assessments - Cyber Hygiene
Cybersecurity and Infrastructure Security Agency
vulnerability@cisa.dhs.gov

----changelog----
03/28/2017
* Fixed: Compliance scores in the "Executive Summary" now account for preloaded domains. Preloading is OMB's preferred method for HSTS compliance.

02/15/2017
* Fixed an issue where some hostnames would appear twice in pshtt-results.csv
* Fixed: A local caching error caused domains that have been HSTS preloaded after December 19th, 2016 to be reported incorrectly
* Known issue: Compliance scores in the "Executive Summary" section are not yet accounting for preloaded domains

01/25/2017
* Fixed: A flaw in the report logic would sometimes cause the "Results" section of the PDF to inaccurately represent raw pshtt scores. This error would also represent domains that were "HSTS Preload Ready" or "HSTS Preload Pending" as preloaded (a checkmark).
* Added: The report will now represent domains with "bad chain" errors (but not hostname or expired certificate errors) that otherwise satisfy M-15-13 as compliant. This is in line with M-15-13 not requiring the use of a particular certificate authority
--------------------
"""
                self.assertEqual(part.get_payload(), body)
            elif part.get_content_type() == "text/html":
                html_body = """<html>
<head></head>
<body>
<div style=""font-size:14.5"">
<p>Greetings Clarke of Kent (CLARKE),</p>
<p>Attached is your latest HTTPS Report.</p>
<p>This report is intended to assist your agency in complying with OMB <a href="https://https.cio.gov">M-15-13</a> and CISA <a href="https://cyber.dhs.gov/bod/18-01/">Binding Operational Directive 18-01</a>.</p>
<p>This report includes all second-level .gov domains your agency owns and many known subdomains. Subdomains are gleaned from Cyber Hygiene scans, the General Services Administration's <a href="https://analytics.usa.gov/">Digital Analytics Program</a>, <a href=https://censys.io>Censys.io</a>, and data from the <a href="http://eotarchive.cdlib.org/">End of Term Web Archive</a>. The data in this report comes from a <b>scan that took place on December 15, 2001.</b></p>
<p>The embedded CSV, pshtt-results.csv, contains the raw scores for compliance. <i>For domains where &ldquo;Live&rdquo; == &ldquo;True&rdquo;</i>, when &ldquo;Domain Supports HTTPS&rdquo;, &ldquo;Domain Enforces HTTPS&rdquo;, and &ldquo;Domain Uses Strong HSTS&rdquo; are all &ldquo;True&rdquo;, OR where &ldquo;HSTS Base Domain Preloaded&rdquo; is &ldquo;True&rdquo;, that domain is M-15-13 compliant. Domains where &ldquo;Live&rdquo; == &ldquo;False&rdquo; are not web-responsive and do not fall under M-15-13's scope.</p>
<p>We welcome your feedback and questions.</p>
<p>Cheers,<br>
CISA Cyber Assessments - Cyber Hygiene<br><br />
Cybersecurity and Infrastructure Security Agency<br />
<a href=""mailto:vulnerability@cisa.dhs.gov""> vulnerability@cisa.dhs.gov </a>
</p>
</div>
</p><br>
<p>----changelog----</p>
<p><i>03/28/2017</i></p>
<p><b>* Fixed:</b> Compliance scores in the &ldquo;Executive Summary&rdquo; now account for preloaded domains. Preloading is OMB's <a href="https://https.cio.gov/guide/#options-for-hsts-compliance">preferred method</a> for HSTS compliance.</p></p>
<p><i>02/15/2017</i></p>
<p><b>* Fixed</b> an issue where some hostnames would appear twice in<b> pshtt-results.csv <br>
* Fixed: </b>A local caching error caused domains that have been HSTS preloaded after December 19th, 2016 to be reported incorrectly<br>
<b>* Known issue</b>: Compliance scores in the &ldquo;Executive Summary&rdquo; section are not yet accounting for preloaded domains</p>
<p><i>01/25/2017</i></p>
<p><b>* Fixed</b>: A flaw in the report logic would sometimes cause the &ldquo;Results&rdquo; section of the PDF to inaccurately represent raw pshtt scores. This error would also represent domains that were &ldquo;HSTS Preload Ready&rdquo; or &ldquo;HSTS Preload Pending&rdquo; as preloaded (a checkmark).<br>
<b>* Added</b>: The report will now represent domains with &ldquo;bad chain&rdquo; errors (but not hostname or expired certificate errors) that otherwise satisfy M-15-13 as compliant. This is in line with M-15-13 <a href="https://https.cio.gov/certificates/#are-there-federal-restrictions-on-acceptable-certificate-authorities-to-use%3f">not requiring the use of a particular certificate authority</a>.</p>
<p>--------------------</p>
</body>
</html>
"""
                self.assertEqual(part.get_payload(), html_body)


if __name__ == "__main__":
    unittest.main()
