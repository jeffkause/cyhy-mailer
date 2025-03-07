"""This module contains the TmailMessage class."""

# Third-Party Libraries
import chevron

# cisagov Libraries
from cyhy.mailer.Message import Message
from cyhy.mailer.ReportMessage import ReportMessage


class TmailMessage(ReportMessage):
    """An email message with a Trustworthy Email report PDF attachment.

    Static attributes
    -----------------
    Subject : str
        The mustache template to use when constructing the message
        subject.

    TextBody : str
        The mustache template to use when constructing the plain text
        message body.

    HtmlBody : str
        The mustache template to use when constructing the HTML
        message body.

    """

    Subject = "{{acronym}} - Trustworthy Email Report - {{report_date}} Results"

    TextBody = """Greetings {{name}} ({{acronym}}),

Attached is your Trustworthy Email Report. This report presents your organization's support of SPF and DMARC, two email authentication standards, as published at your .gov domains. The data in this report comes from a scan that took place on {{report_date}}.

CISA Binding Operational Directive 18-01 requires your agency to take certain actions relevant to the data in this report:
* Within 90 days of BOD issuance, configure all second-level domains to have valid SPF/DMARC records, with at minimum a DMARC policy of "p=none" and at least one address defined as a recipient of aggregate and/or failure reports.
* Within one year of BOD issuance, set a DMARC policy of "reject" for all second-level domains and mail-sending hosts.
* The Directive additionally requires all internet-facing mail servers to offer STARTTLS. This data will be represented in the Trustworthy Email Report in December.

Raw results in this Report are available as a CSV in the Appendix, which includes error messages. Note that this report includes data from second-level .gov domains, but the Directive's scope includes any domain suffix.

The actions the Directive requires increase the security of emails in transit and makes it easier to detect emails that attempt to spoof .gov domains. This protects intra-government users and the general public equally. See https://cyber.dhs.gov/bod/18-01/#introduction-to-email-authentication for more information about email authentication, as well as https://cyber.dhs.gov/bod/18-01/#compliance-guide and https://cyber.dhs.gov/bod/18-01/#frequently-asked-questions for a compliance guide and FAQ, respectively.

If you believe our reporting or methodology is in error, let us know. If the flaw appears tool-related, we encourage you to file an issue on our open-source scanner at https://github.com/cisagov/trustymail.

We welcome your feedback and questions.

Cheers,
CISA Cyber Assessments - Cyber Hygiene
Cybersecurity and Infrastructure Security Agency
vulnerability@cisa.dhs.gov

----changelog----
12/11/2017
* Known issue: The fed.us TLD is inaccurately represented in some reports.
03/29/2019
* If an SMTP-responsive hostname does not have an SPF record set, but it is covered by a valid DMARC record with a policy of reject, we now count the hostname as compliant with respect to SPF.  This change is being made to more closely align with the exact language in BOD 18-01.  As a result, users may see an increase in SPF record compliance scores.
-----------------
"""

    HtmlBody = """<html>
<head></head>
<body>
<div style=""font-size:14.5"">
<p>Greetings {{name}} ({{acronym}}),</p>
<p>Attached is your <b>Trustworthy Email Report</b>. This report presents your organization's support of SPF and DMARC, two email authentication standards, as published at your .gov domains. The data in this report comes from a <b>scan that took place on {{report_date}}.</b></p>
<p><a href="https://cyber.dhs.gov/bod/18-01/">CISA Binding Operational Directive 18-01</a> requires your agency to take certain actions relevant to the data in this report:</p>
<ul>
<li>Within 90 days of BOD issuance, configure all second-level domains to have valid SPF/DMARC records, with at minimum a DMARC policy of &ldquo;p=none&rdquo; and at least one address defined as a recipient of aggregate and/or failure reports.</li>
<li>Within one year of BOD issuance, set a DMARC policy of &ldquo;reject&rdquo; for all second-level domains and mail-sending hosts.</li>
<li>(The Directive additionally requires all internet-facing mail servers to offer STARTTLS. This data will be represented in the Trustworthy Email Report in December.</li>
</ul>
</p>
<p>Raw results in this Report are available as a CSV in the Appendix, which includes error messages. Note that this report includes data from second-level .gov domains, but the Directive's <a href="https://cyber.dhs.gov/bod/18-01/#what-is-the-scope-of-bod-18-01">scope includes any domain suffix</a>.</p>
<p>The actions the Directive requires increases the security of emails in transit and makes it easier to detect emails that attempt to spoof .gov domains. This protects intra-government users and the general public equally. See <a href="https://cyber.dhs.gov/bod/18-01/#introduction-to-email-authentication">cyber.dhs.gov/bod/18-01/#introduction-to-email-authentication</a> for more information about email authentication, as well as <a href="https://cyber.dhs.gov/bod/18-01/#compliance-guide">cyber.dhs.gov/bod/18-01/#compliance-guide</a> and <a href="https://cyber.dhs.gov/bod/18-01/#frequently-asked-questions">cyber.dhs.gov/bod/18-01/#frequently-asked-questions</a> for a compliance guide and FAQ, respectively.</p>
<p>If you believe our reporting or methodology is in error, let us know. If the flaw appears tool-related, we encourage you to <a href="https://github.com/cisagov/trustymail">file an issue</a> on our open-source scanner.</p>
<p>We welcome your feedback and questions.</p>
<p>Cheers,<br>
CISA Cyber Assessments - Cyber Hygiene<br><br />
Cybersecurity and Infrastructure Security Agency<br />
<a href=""mailto:vulnerability@cisa.dhs.gov"">vulnerability@cisa.dhs.gov</a></p>
</div></p><br>
<p>----changelog----</p>
<p><i>12/11/2017</i></p>
<b>* Known issue:</b> The fed.us TLD is inaccurately represented in some reports.</p>
<p><i>03/29/2019</i></p>
<b>* </b> If an SMTP-responsive hostname does not have an SPF record set, but it is covered by a valid DMARC record with a policy of reject, we now count the hostname as compliant with respect to SPF.  This change is being made to more closely align with the exact language in BOD 18-01.  As a result, users may see an increase in SPF record compliance scores. </p>
<p>--------------------</p>
</body>
</html>
"""

    def __init__(
        self,
        to_addrs,
        pdf_filename,
        entity_acronym,
        entity_name,
        report_date,
        from_addr=Message.DefaultFrom,
        cc_addrs=Message.DefaultCc,
        bcc_addrs=Message.DefaultBcc,
    ):
        """Construct an instance.

        Parameters
        ----------
        to_addrs : array of str
            An array of string objects, each of which is an email
            address to which this message should be sent.

        pdf_filename : str
            The filename of the PDF file that is the Trustworthy Email
            report corresponding to this message.

        entity_acronym : str
            The acronym used by the entity corresponding to the
            Trustworthy Email report attachment.

        entity_name : str
            The name of the entity corresponding to the Trustworthy Email
            report attachment.

        report_date : str
            The date corresponding to the Trustworthy Email report
            attachment.  We have been using dates of the form December
            12, 2017.

        from_addr : str
            The email address from which this message is to be sent.

        cc_addrs : array of str
            An array of string objects, each of which is a CC email
            address to which this message should be sent.

        bcc_addrs : array of str
            An array of string objects, each of which is a BCC email
            address to which this message should be sent.

        """
        # This is the data mustache will use to render the templates
        mustache_data = {
            "acronym": entity_acronym,
            "name": entity_name,
            "report_date": report_date,
        }

        # Render the templates
        subject = chevron.render(TmailMessage.Subject, mustache_data)
        text_body = chevron.render(TmailMessage.TextBody, mustache_data)
        html_body = chevron.render(TmailMessage.HtmlBody, mustache_data)

        ReportMessage.__init__(
            self,
            to_addrs,
            subject,
            text_body,
            html_body,
            pdf_filename,
            from_addr,
            cc_addrs,
            bcc_addrs,
        )
