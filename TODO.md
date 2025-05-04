# TODO: Post-Rebranding Verification Checklist

After performing the GAIuS → Mythral and Intelligent Artifacts → DubPrime rebranding, use this checklist to ensure the project still works as expected.

## 1. Automated Testing
- [ ] Run all existing automated tests (unit, integration, end-to-end)
- [ ] Add or update tests if necessary to cover renamed components
- [ ] Ensure all tests pass after the rename

## 2. Manual Spot Checks
- [ ] Open the application (web, CLI, etc.) and verify key workflows
- [ ] Check for broken links, missing images, or UI references to old names
- [ ] Manually review critical features for regressions

## 3. Build & Lint
- [ ] Run the build process (e.g., `npm run build`, `make`, etc.)
- [ ] Run linters (e.g., `flake8`, `eslint`) to catch unresolved imports or typos

## 4. Search for Missed References
- [ ] Search the codebase for any remaining instances of `GAIuS`, `gaius`, `Intelligent Artifacts`, or `intelligent artifacts`
- [ ] Address any missed references in code, configs, or documentation

## 5. Check File/Directory Structure
- [ ] Verify that renamed files and directories are referenced correctly in imports, links, and configs
- [ ] Ensure no broken imports or file-not-found errors

## 6. Documentation & Metadata
- [ ] Review README, documentation, and metadata files for any missed branding
- [ ] Update screenshots or images if they contain old branding

## 7. Version Control & Review
- [ ] Commit all changes in a new branch
- [ ] Use `git diff` to review all changes
- [ ] Request a peer review of the changes if possible

---

**Tip:** If you do not have automated tests, consider creating a minimal test script or manually verifying the most important workflows. 