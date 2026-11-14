"""Core capability attenuation proxy implementation."""
import time
from typing import Set, Dict, Any, Optional

class CapabilityToken:
    def __init__(self, token_id: str, allowed_actions: Set[str], depth: int = 0, expires_at: float = 0.0):
        self.token_id = token_id
        self.allowed_actions = allowed_actions
        self.depth = depth
        self.expires_at = expires_at

    @property
    def is_valid(self) -> bool:
        if self.expires_at > 0 and time.time() > self.expires_at:
            return False
        return True

class AttenuationRule:
    @staticmethod
    def attenuate(parent_token: CapabilityToken, requested_actions: Set[str], ttl_seconds: float = 60.0) -> CapabilityToken:
        # Attenuation can only shrink permissions, never expand
        narrowed = parent_token.allowed_actions.intersection(requested_actions)
        new_token_id = f"{parent_token.token_id}_sub_{parent_token.depth + 1}"
        exp = time.time() + ttl_seconds
        return CapabilityToken(new_token_id, narrowed, depth=parent_token.depth + 1, expires_at=exp)

class CapabilityAttenuationProxy:
    def __init__(self):
        self.audit_log: list = []

    def verify_and_dispatch(self, token: CapabilityToken, action: str) -> bool:
        if not token.is_valid:
            self.audit_log.append({"token_id": token.token_id, "action": action, "verdict": "EXPIRED"})
            return False

        if action in token.allowed_actions:
            self.audit_log.append({"token_id": token.token_id, "action": action, "verdict": "ALLOWED"})
            return True
        else:
            self.audit_log.append({"token_id": token.token_id, "action": action, "verdict": "DENIED_UNAUTHORIZED"})
            return False
