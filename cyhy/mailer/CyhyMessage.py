"""This module contains the CyhyMessage class."""

# Third-Party Libraries
import chevron

# cisagov Libraries
from cyhy.mailer.Message import Message
from cyhy.mailer.ReportMessage import ReportMessage


class CyhyMessage(ReportMessage):
    """An email message with a CYHY report PDF attachment.

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

    Subject = "{{acronym}} - Cyber Hygiene Report - {{report_date}} Results"

    TextBody = """Greetings {{name}} ({{acronym}}),

The Cyber Hygiene scan results are attached for your review. Same password as before. (If this is your first report and you have yet to receive a password, please let us know.)

{{#has_tech_pocs}}
Note: CISA has the following information listed as the Technical Points of Contact for {{acronym}}:

{{#tech_pocs}}
Name:  {{name}}
Email:  {{email}}

{{/tech_pocs}}
Please request the report password from a Technical Point of Contact and route all other requests through a Technical POC. Should a Technical Point of Contact listed above no longer be with {{acronym}}, please contact vulnerability@cisa.dhs.gov with updated information.

{{/has_tech_pocs}}
If you have any questions, please contact our office.

Cheers,
CISA Cyber Assessments - Cyber Hygiene
Cybersecurity and Infrastructure Security Agency
vulnerability@cisa.dhs.gov

WARNING: This document is FOR OFFICIAL USE ONLY (FOUO). It contains information that may be exempt from public release under the Freedom of Information Act (5 U.S.G. 552). It is to be controlled, stored, handled, transmitted, distributed, and disposed of in accordance with CISA policy relating to FOUO information and is not to be released to the public or other personnel who do not have a valid 'need-to-know' without prior approval of an authorized CISA official.
"""

    HtmlBody = """<html>
<head></head>
<body>
<p>Greetings {{name}} ({{acronym}}),</p>

<p>The Cyber Hygiene scan results are attached for your review. Same password as before. (If this is your first report and you have yet to receive a password, please let us know.)</p>

{{#has_tech_pocs}}
<p>Note: CISA has the following information listed as the Technical Points of Contact for {{acronym}}:</p>

{{#tech_pocs}}
<p>
Name:  {{name}}<br>
Email:  {{email}}<br>
</p>
{{/tech_pocs}}

<p>Please request the report password from a Technical Point of Contact and route all other requests through a Technical POC. Should a Technical Point of Contact listed above no longer be with {{acronym}}, please contact <a href="mailto:vulnerability@cisa.dhs.gov">vulnerability@cisa.dhs.gov</a> with updated information.</p>

{{/has_tech_pocs}}
<p>If you have any questions, please contact our office.</p>

<p>Cheers,<br>
CISA Cyber Assessments - Cyber Hygiene<br>
Cybersecurity and Infrastructure Security Agency<br>
<a href="mailto:vulnerability@cisa.dhs.gov">vulnerability@cisa.dhs.gov</a></p>

<p>WARNING: This document is FOR OFFICIAL USE ONLY (FOUO). It contains information that may be exempt from public release under the Freedom of Information Act (5 U.S.G. 552). It is to be controlled, stored, handled, transmitted, distributed, and disposed of in accordance with CISA policy relating to FOUO information and is not to be released to the public or other personnel who do not have a valid 'need-to-know' without prior approval of an authorized CISA official.</p>
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
        tech_pocs,
        from_addr=Message.DefaultFrom,
        cc_addrs=Message.DefaultCc,
        bcc_addrs=Message.DefaultBcc,
    ):
        """Construct an instance.

        Parameters
        ----------
        to_addrs : list of str
            A list of string objects, each of which is an email
            address to which this message should be sent.

        pdf_filename : str
            The filename of the PDF file that is the CYHY report
            corresponding to this message.

        entity_acronym : str
            The acronym used by the entity corresponding to the CYHY
            report attachment.

        entity_name : str
            The name of the entity corresponding to the CYHY report
            attachment.

        report_date : str
            The date corresponding to the CYHY report attachment.  We
            have been using dates of the form December 12, 2017.

        tech_pocs : list of dict
            A list of dicts, each containing a "name" and an "email"
            key.  The corresponding values correspond to the name and
            email of a technical POC for the entity corresponding to
            the CYHY report attachment.  If there are no technical
            POCs for the entity then this parameter should be an empty
            list.

        from_addr : str
            The email address from which this message is to be sent.

        cc_addrs : list of str
            A list of string objects, each of which is a CC email
            address to which this message should be sent.

        bcc_addrs : list of str
            A list of string objects, each of which is a BCC email
            address to which this message should be sent.

        """
        # This is the data mustache will use to render the templates
        mustache_data = {
            "acronym": entity_acronym,
            "has_tech_pocs": len(tech_pocs) != 0,
            "name": entity_name,
            "report_date": report_date,
            "tech_pocs": tech_pocs,
        }

        # Render the templates
        subject = chevron.render(CyhyMessage.Subject, mustache_data)
        text_body = chevron.render(CyhyMessage.TextBody, mustache_data)
        html_body = chevron.render(CyhyMessage.HtmlBody, mustache_data)

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
