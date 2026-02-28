# AI Employee - Bronze Tier Project

## Project Overview

This is a **Bronze Tier** hackathon project for building a **Personal AI Employee** (Digital FTE - Full-Time Equivalent). The project creates an autonomous AI agent powered by **Claude Code** and **Obsidian** that proactively manages personal and business affairs 24/7.

**Architecture Philosophy:** Local-first, agent-driven, human-in-the-loop automation.

**Tagline:** *Your life and business on autopilot.*

### Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **The Brain** | Claude Code | Reasoning engine for task execution |
| **The Memory/GUI** | Obsidian (Markdown) | Dashboard and long-term memory |
| **The Senses** | Python Watcher Scripts | Monitor Gmail, WhatsApp, filesystems |
| **The Hands** | MCP Servers | External actions (browser automation, email, etc.) |

### Key Features

- **Watcher Architecture:** Lightweight Python scripts monitor inputs and create actionable `.md` files in `/Needs_Action` folder
- **Ralph Wiggum Loop:** Persistence pattern that keeps Claude iterating until tasks are complete
- **Human-in-the-Loop:** Sensitive actions require approval via file movement (`/Pending_Approval` → `/Approved`)
- **Business Handover:** Autonomous weekly audits generating "Monday Morning CEO Briefing"

## Directory Structure

```
BronzeTier/
├── .qwen/skills/
│   └── browsing-with-playwright/    # Playwright MCP browser automation skill
│       ├── SKILL.md                 # Skill documentation
│       ├── references/
│       │   └── playwright-tools.md  # Complete MCP tool reference
│       └── scripts/
│           ├── start-server.sh      # Start Playwright MCP server
│           ├── stop-server.sh       # Stop Playwright MCP server
│           ├── mcp-client.py        # MCP client for tool invocation
│           └── verify.py            # Server health verification
├── scripts/                         # (To be created) Watcher scripts
├── Vault/                          # (To be created) Obsidian vault
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Done/
│   ├── Pending_Approval/
│   └── Approved/
├── skills-lock.json                # Qwen skills configuration
└── Personal AI Employee Hackathon 0_....md  # Full hackathon blueprint
```

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Claude Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts & orchestration |
| Node.js | v24+ LTS | MCP servers |

### Setup Commands

```bash
# 1. Create Obsidian vault structure
mkdir -p Vault/{Inbox,Needs_Action,Done,Pending_Approval,Approved}

# 2. Initialize Python environment (using UV)
uv init
uv add watchdog google-api-python-client playwright

# 3. Install Playwright browsers
npx playwright install

# 4. Start Playwright MCP server (for browser automation)
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# 5. Verify server is running
python .qwen/skills/browsing-with-playwright/scripts/verify.py
```

### Running Watcher Scripts

```bash
# Gmail watcher (example - requires Gmail API credentials)
python scripts/gmail_watcher.py

# File system watcher
python scripts/filesystem_watcher.py

# WhatsApp watcher (Playwright-based)
python scripts/whatsapp_watcher.py
```

### Starting Claude Code with Ralph Wiggum Loop

```bash
# Start autonomous task processing
claude "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

## Development Conventions

### File Naming Patterns

| Pattern | Purpose |
|---------|---------|
| `*_watcher.py` | Sentinel scripts monitoring external inputs |
| `*_mcp.py` | MCP server implementations |
| `*.md` in `Needs_Action/` | Actionable items for Claude |
| `Plan.md` | Multi-step task plans created by Claude |

### Agent Skills

All AI functionality should be implemented as **[Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)** - reusable, promptable capabilities that Claude can invoke.

### Human-in-the-Loop Pattern

For sensitive actions (payments, sending messages):

1. Claude creates approval request: `/Pending_Approval/PAYMENT_Client_A_2026-01-07.md`
2. User reviews and moves file to `/Approved/`
3. Orchestrator triggers actual MCP action
4. Result logged to `/Done/`

### Watcher Script Template

All watchers follow the `BaseWatcher` pattern:

```python
from abc import ABC, abstractmethod
from pathlib import Path

class BaseWatcher(ABC):
    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass

    def run(self):
        """Main loop - check every N seconds"""
        while True:
            items = self.check_for_updates()
            for item in items:
                self.create_action_file(item)
            time.sleep(check_interval)
```

## Testing Practices

- **Verification Scripts:** Each MCP server has a `verify.py` script
- **Watcher Testing:** Test with sample input files in `/Inbox/`
- **Approval Workflow:** Test with mock approval requests

## Key Documentation

- [`Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md) - Complete hackathon blueprint with architecture details
- [`SKILL.md`](./.qwen/skills/browsing-with-playwright/SKILL.md) - Playwright MCP usage guide
- [`playwright-tools.md`](./.qwen/skills/browsing-with-playwright/references/playwright-tools.md) - Complete MCP tool reference

## Tier Progression

| Tier | Requirements | Estimated Time |
|------|-------------|----------------|
| **Bronze** | Obsidian vault, 1 watcher, Claude reading/writing | 8-12 hours |
| **Silver** | 2+ watchers, MCP server, HITL approval | 20-30 hours |
| **Gold** | Full integration, Odoo accounting, Ralph Wiggum loop | 40+ hours |
| **Platinum** | Cloud deployment, 24/7 operation, A2A sync | 60+ hours |

## Current Status: Bronze Tier ✅ COMPLETE

This directory contains:
- ✅ Hackathon blueprint documentation
- ✅ Playwright MCP skill (browser automation)
- ✅ Skills configuration (`skills-lock.json`)
- ✅ Watcher scripts (base_watcher.py, filesystem_watcher.py, orchestrator.py)
- ✅ Obsidian vault structure with all folders
- ✅ Core Markdown files (Dashboard.md, Company_Handbook.md, Business_Goals.md)
- ✅ README.md with setup and usage instructions
- ✅ Verification script (scripts/verify.py)
- ⏳ Claude Code (requires separate npm install and subscription)
