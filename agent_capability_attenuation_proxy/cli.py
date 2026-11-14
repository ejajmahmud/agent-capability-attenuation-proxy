"""CLI for agent-capability-attenuation-proxy."""
import argparse
import sys
from .core import CapabilityAttenuationProxy, CapabilityToken, AttenuationRule

def main():
    parser = argparse.ArgumentParser(description="Agent Capability Attenuation Proxy CLI")
    parser.add_argument("--demo", action="store_true", help="Run capability attenuation proxy demo")
    args = parser.parse_args()

    if args.demo:
        proxy = CapabilityAttenuationProxy()
        root_token = CapabilityToken("root_admin", {"read_file", "write_file", "execute_bash", "delete_file"})
        # Subagent only gets read_file
        sub_token = AttenuationRule.attenuate(root_token, {"read_file"})

        print(f"[+] Root token scopes: {root_token.allowed_actions}")
        print(f"[+] Attenuated subagent scopes: {sub_token.allowed_actions}")

        v1 = proxy.verify_and_dispatch(sub_token, "read_file")
        v2 = proxy.verify_and_dispatch(sub_token, "delete_file")

        print(f"[+] Action 'read_file' result: {v1}")
        print(f"[+] Action 'delete_file' result: {v2} (Privilege Escalation Blocked)")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
