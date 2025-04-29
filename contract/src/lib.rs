use anchor_lang::prelude::*;
use anchor_spl::token::{self, Mint, Token, TokenAccount, MintTo, InitializeMint, InitializeAccount};
use anchor_spl::associated_token::AssociatedToken;

declare_id!("91DtZwZYsgQdFyqbv3D9WyeCv8Egro8KWPhuc7yxZQMc");

#[program]
pub mod nft_project {
    use super::*;

    pub fn create_mint(
        ctx: Context<CreateMint>,
        _name: String,
        _symbol: String,
        _uri: String,
    ) -> Result<()> {
        let cpi_accounts = InitializeMint {
            mint: ctx.accounts.mint.to_account_info(),
            rent: ctx.accounts.rent.to_account_info(),
        };
        let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
        token::initialize_mint(cpi_ctx, 0, &ctx.accounts.authority.key(), Some(&ctx.accounts.authority.key()))?;
        Ok(())
    }

    pub fn mint_nft(ctx: Context<MintNFT>) -> Result<()> {
        let cpi_accounts = MintTo {
            mint: ctx.accounts.mint.to_account_info(),
            to: ctx.accounts.token_account.to_account_info(),
            authority: ctx.accounts.authority.to_account_info(),
        };
        let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
        token::mint_to(cpi_ctx, 1)?;
        Ok(())
    }

    pub fn list_nft(ctx: Context<ListNFT>, price: u64) -> Result<()> {
        ctx.accounts.sale_state.price = price;
        ctx.accounts.sale_state.seller = ctx.accounts.authority.key();
        ctx.accounts.sale_state.mint = ctx.accounts.mint.key();
        Ok(())
    }
}

#[derive(Accounts)]
pub struct CreateMint<'info> {
    #[account(init, payer = authority, space = 82, mint::decimals = 0, mint::authority = authority, mint::freeze_authority = authority)]
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub rent: Sysvar<'info, Rent>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct MintNFT<'info> {
    #[account(mut)]
    pub mint: Account<'info, Mint>,
    #[account(init_if_needed, payer = authority, associated_token::mint = mint, associated_token::authority = authority)]
    pub token_account: Account<'info, TokenAccount>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct ListNFT<'info> {
    #[account(init, payer = authority, space = 8 + 32 + 32 + 8)]
    pub sale_state: Account<'info, SaleState>,
    #[account(mut)]
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct SaleState {
    pub mint: Pubkey,
    pub seller: Pubkey,
    pub price: u64,
}
