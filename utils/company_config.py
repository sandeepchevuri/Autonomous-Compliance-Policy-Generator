import yaml
import os

def load_company_profile(path:str=None)->dict:
    """Load company profile from a YAML file."""
    if path is None:
        path=os.path.join(os.path.dirname(__file__), "..", "company_profile.yaml")
    with open(path, "r") as f:
        profile=yaml.safe_load(f)
    return profile

    
def get_company_context_prompt(profile:dict)->str:
    """Convert company profile to a prompt-friendly string."""
    company = profile.get("company", {})
    compliance = profile.get("compliance", {})
    org = profile.get("organization", {})
    data = profile.get("data", {})
    systems = profile.get("systems", {})
    contacts = profile.get("contacts", {})
    vendors = profile.get("vendors", [])

    context=f"""
    === COMPANY CONTEXT ===

Company Name: {company.get('name', 'N/A')}
Legal Entity: {company.get('legal_entity', 'N/A')}
Industry: {company.get('industry', 'N/A')}

Regulatory Applicability:
- HIPAA Covered Entity: {compliance.get('is_hipaa_covered_entity', False)}
- HIPAA Business Associate: {compliance.get('is_hipaa_business_associate', False)}
- GDPR Applicable: {compliance.get('gdpr_applicable', False)}
- SOC2 Required: {compliance.get('soc2_required', False)}
- ISO27001 Certified: {compliance.get('iso27001_certified', False)}

Organization:
- Employees: {org.get('employee_count', 'N/A')}
- Locations: {', '.join(org.get('locations', []))}

Data Processed:
{chr(10).join('- ' + d for d in data.get('types_processed', []))}

Data Subjects:
{chr(10).join('- ' + d for d in data.get('data_subjects', []))}

Systems & Infrastructure:
- Cloud: {', '.join(systems.get('cloud_providers', []))}
- Applications: {', '.join(systems.get('applications', []))}
- Security Controls: {', '.join(systems.get('security_controls', []))}

Key Contacts:
- DPO: {contacts.get('dpo', {}).get('name', 'N/A')} ({contacts.get('dpo', {}).get('email', 'N/A')})
- CISO: {contacts.get('ciso', {}).get('name', 'N/A')} ({contacts.get('ciso', {}).get('email', 'N/A')})
- Privacy Officer: {contacts.get('privacy_officer', {}).get('name', 'N/A')} ({contacts.get('privacy_officer', {}).get('email', 'N/A')})
- Legal: {contacts.get('legal', {}).get('name', 'N/A')} ({contacts.get('legal', {}).get('email', 'N/A')})

Vendors:
{chr(10).join('- ' + v.get('name', '') + ' (' + v.get('service', '') + ')' for v in vendors)}

=== END COMPANY CONTEXT ===
"""

    return context