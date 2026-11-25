"""Inference engine: forward chaining + partial-match ranking + follow-up questions."""
from knowledge_base import RULES


class InferenceEngine:
    def __init__(self, rules=RULES):
        self.rules = rules

    def forward_chain(self, symptoms):
        """Fire every rule whose conditions are all known. Derived diagnoses are
        added to working memory as '@Diagnosis' so later rules can chain on them.
        Returns (fired_rules, working_memory)."""
        memory = set(symptoms)
        fired = []
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule in fired:
                    continue
                if all(c in memory for c in rule.conditions):
                    fired.append(rule)
                    memory.add("@" + rule.conclusion)
                    changed = True
        return fired, memory

    def partial_matches(self, memory, denied=(), min_ratio=0.5):
        """Rules not fully satisfied but with enough evidence, best first."""
        fired = {"@" + r.conclusion for r in self.rules if all(c in memory for c in r.conditions)}
        out = []
        for rule in self.rules:
            if "@" + rule.conclusion in fired:
                continue
            if any(c in denied for c in rule.conditions):
                continue
            matched = [c for c in rule.conditions if c in memory]
            if not matched:
                continue
            ratio = len(matched) / len(rule.conditions)
            if ratio >= min_ratio:
                missing = [c for c in rule.conditions if c not in memory]
                out.append((rule, matched, missing, ratio))
        out.sort(key=lambda x: (-x[3], -len(x[1])))
        return out

    def next_question(self, memory, denied=(), asked=()):
        """Pick the most useful symptom to ask about next (from the best partial rule)."""
        for rule, _, missing, _ in self.partial_matches(memory, denied):
            for cond in missing:
                if not cond.startswith("@") and cond not in asked and cond not in denied:
                    return cond, rule
        return None, None

    @staticmethod
    def explain(rule):
        return f"{rule.id}: IF {' AND '.join(c.lstrip('@') for c in rule.conditions)} THEN {rule.conclusion}"
