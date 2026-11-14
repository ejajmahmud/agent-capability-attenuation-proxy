"""Unit tests for agent-capability-attenuation-proxy."""
import unittest
from agent_capability_attenuation_proxy.core import CapabilityAttenuationProxy, CapabilityToken, AttenuationRule

class TestCapabilityAttenuationProxy(unittest.TestCase):
    def setUp(self):
        self.proxy = CapabilityAttenuationProxy()

    def test_attenuation_cannot_escalate(self):
        parent = CapabilityToken("tok1", {"read", "write"})
        # Attempt to request "admin" which parent does not have
        sub = AttenuationRule.attenuate(parent, {"read", "admin"})
        self.assertEqual(sub.allowed_actions, {"read"})

    def test_allowed_and_denied_dispatch(self):
        token = CapabilityToken("tok2", {"grep", "find"})
        self.assertTrue(self.proxy.verify_and_dispatch(token, "grep"))
        self.assertFalse(self.proxy.verify_and_dispatch(token, "rm"))
